#!/usr/bin/env python3
"""Organize existing public red-team reference material into the CBBH topics.

Never executes code from source repositories. Keeps existing CBBH notes intact.
Images are copied only when referenced, and internal Markdown links are rewritten.
"""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import posixpath
import re
import shutil
import subprocess
import tempfile
import unicodedata
from urllib.parse import unquote, urlsplit

BASE = Path(__file__).resolve().parents[2]
REPOS = [
    ("notes", "1"),
    ("pentestNotes", "master"),
    ("writeups", "main"),
    ("web", "main"),
    ("bugbounty-notes", "main"),
]
MEDIA_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp"}
INDEX_SECTIONS = [
    ("Active-Directory/Advanced", "Active Directory — técnicas avanzadas"),
    ("Active-Directory/Field-Notes", "Active Directory — consultas y notas de campo"),
    ("Privilege-Escalation", "Escalada de privilegios Linux y Windows"),
    ("Pivoting", "Pivoting, tunneling y port forwarding"),
    ("Network-Pentesting/Service-Reference", "Enumeración de servicios"),
    ("Web-Security/CMS/Reference", "CMS y aplicaciones"),
    ("Web-Security/Field-Notes", "Explotación web — ejemplos"),
    ("Web-Security/Techniques", "Técnicas web"),
    ("Labs-and-Writeups/Proving-Grounds-Practice", "Proving Grounds Practice"),
    ("Wireless", "Wi-Fi"),
]
new_pages: set[Path] = set()
media_sha_to_path: dict[str, Path] = {}
warnings: list[str] = []


def run(cmd, cwd=None):
    print("+", " ".join(map(str, cmd)), flush=True)
    subprocess.run(cmd, cwd=cwd, check=True)


def slug(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = s.encode("ascii", "ignore").decode("ascii").lower()
    s = re.sub(r"[^a-z0-9._-]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-._") or "untitled"


def make_path(parts):
    names = []
    for part in parts:
        if part.lower() == "readme.md":
            names.append("overview.md")
        elif part.lower().endswith(".md"):
            names.append(slug(part[:-3]) + ".md")
        else:
            names.append(slug(part))
    return Path(*names)


def destination(repo, path: Path):
    parts = path.parts
    first = parts[0].lower()
    rest = parts[1:]
    if repo == "notes":
        prefixes = {
            "active-directory": "Active-Directory/Advanced",
            "enumeration": "Enumeration/Advanced",
            "file-transfers": "Tools/File-Transfers",
            "password-attacks": "Password-Attacks/Advanced",
            "pivoting-tunneling-and-port-forwarding": "Pivoting",
            "privesc": "Privilege-Escalation",
            "shells": "Tools/Shells/Advanced",
            "web": "Web-Security/Techniques",
            "write-ups": "Labs-and-Writeups/Proving-Grounds-Play/Reference",
        }
        if first in prefixes:
            return Path(prefixes[first]) / make_path(rest)
        if path.name.lower() == "metasploit.md":
            return Path("Tools/metasploit-notes.md")
        return Path("Enumeration/Advanced") / make_path(parts)
    if repo == "pentestNotes":
        prefixes = {
            "active directory": "Active-Directory/Field-Notes",
            "android": "Mobile-Security/Advanced",
            "burpsuite": "Tools/Burpsuite/Advanced",
            "cms - frameworks - etc": "Web-Security/CMS/Reference",
            "linux": "Linux/Advanced",
            "passwords attacks": "Password-Attacks/Field-Notes",
            "privesc": "Privilege-Escalation",
            "services": "Network-Pentesting/Service-Reference",
            "shells": "Tools/Shells/Reference",
            "web": "Web-Security/Field-Notes",
            "wifi": "Wireless",
            "windows": "Windows/Field-Notes",
        }
        if first in prefixes:
            return Path(prefixes[first]) / make_path(rest)
        if first == "recon.md":
            return Path("Enumeration/Reconnaissance/recon-reference.md")
        return Path("Tools/Reference") / make_path(parts)
    if repo == "writeups":
        if first == "proving grounds practice":
            return Path("Labs-and-Writeups/Proving-Grounds-Practice") / make_path(rest)
        return Path("Labs-and-Writeups/Proving-Grounds-Practice") / make_path(parts)
    if repo == "web":
        prefixes = {
            "1 - foothold": "Web-Security/Techniques/Foothold",
            "2 - privilege escalation": "Web-Security/Techniques/Authorization",
            "3 - data exfiltration": "Web-Security/Techniques/Server-Side",
            "cbbh": "Web-Security/Advanced",
        }
        if first in prefixes:
            return Path(prefixes[first]) / make_path(rest)
        if first == "burp scanner.md":
            return Path("Tools/Burpsuite/scanner-notes.md")
        return Path("Web-Security/Techniques") / make_path(parts)
    if repo == "bugbounty-notes":
        return Path("Web-Security/Access-Control-and-XXE") / make_path(parts)
    raise ValueError(repo)


def normalize_markdown(text):
    return re.sub(r"\s+", " ", text).strip()


def read_text(path):
    return path.read_text(encoding="utf-8", errors="replace")


def is_content_note(path, text):
    if any(part in {".git", ".obsidian", ".gitbook"} for part in path.parts):
        return False
    if path.name.lower() in {"summary.md", "import.md"}:
        return False
    if len(normalize_markdown(text)) < 40:
        return False
    return True


def relative(from_md: Path, to_target: Path):
    return os.path.relpath(BASE / to_target, start=BASE / from_md.parent).replace(os.sep, "/")


def raw_link_target(repo_path: Path, link: str):
    link = unquote(link.strip().strip("<>"))
    if not link or link.startswith(("#", "data:", "mailto:", "//")):
        return None, ""
    if re.match(r"^[a-z][a-z0-9+.-]*:", link, re.I):
        return None, ""
    split = urlsplit(link)
    raw_path = split.path.replace("\\", "/")
    target = posixpath.normpath(posixpath.join(repo_path.parent.as_posix(), raw_path))
    if target == ".." or target.startswith("../") or target.startswith("/"):
        return None, ""
    suffix = ("?" + split.query if split.query else "") + ("#" + split.fragment if split.fragment else "")
    return Path(target), suffix


def main():
    if not (BASE / ".git").exists():
        raise RuntimeError("Run in the checked-out CBBH repository")
    with tempfile.TemporaryDirectory(prefix="cbbh-refs-") as tmp:
        temp = Path(tmp)
        originals = {}
        docs = {}
        media = {}
        for repo, branch in REPOS:
            folder = temp / repo
            run(["git", "clone", "--quiet", "--depth", "1", "--branch", branch,
                 "https://github.com/20dani09/" + repo + ".git", str(folder)])
            originals[repo] = folder
            docs[repo] = {}
            media[repo] = {}
            for p in folder.rglob("*"):
                if not p.is_file() or p.is_symlink() or ".git" in p.parts:
                    continue
                source_rel = p.relative_to(folder)
                if p.suffix.lower() == ".md":
                    content = read_text(p)
                    if is_content_note(source_rel, content):
                        docs[repo][source_rel] = content
                elif p.suffix.lower() in MEDIA_SUFFIXES:
                    media[repo][source_rel] = p

        # Duplicate detection against existing material (for direct duplicates only).
        old_hashes = {}
        for existing in BASE.rglob("*.md"):
            if ".git" in existing.parts or ".github" in existing.parts:
                continue
            old_hashes.setdefault(hashlib.sha256(normalize_markdown(read_text(existing)).encode()).hexdigest(),
                                  existing.relative_to(BASE))
        for existing in (BASE / "assets").rglob("*") if (BASE / "assets").exists() else ():
            if existing.is_file() and existing.suffix.lower() in MEDIA_SUFFIXES:
                media_sha_to_path.setdefault(hashlib.sha256(existing.read_bytes()).hexdigest(), existing.relative_to(BASE))

        # Map all paths first, so any intra-repo links can be rewritten.
        mappings = {}
        occupied = {p.relative_to(BASE) for p in BASE.rglob("*.md")}
        for repo, _ in REPOS:
            for src, content in docs[repo].items():
                h = hashlib.sha256(normalize_markdown(content).encode()).hexdigest()
                if h in old_hashes:
                    mappings[(repo, src)] = old_hashes[h]
                    continue
                dst = destination(repo, src)
                if dst in occupied:
                    root = dst.with_suffix("")
                    suffix = dst.suffix
                    for n in range(2, 999):
                        candidate = Path(str(root) + f"-{n}" + suffix)
                        if candidate not in occupied:
                            dst = candidate
                            break
                    else:
                        raise RuntimeError(f"Destination collision: {dst}")
                mappings[(repo, src)] = dst
                occupied.add(dst)
                old_hashes[h] = dst

        lookup_media = {}
        for repo, files in media.items():
            by_name = {}
            for src in files:
                by_name.setdefault(src.name.lower(), []).append(src)
            lookup_media[repo] = by_name

        def find_media(repo, src_md, name):
            candidate, _ = raw_link_target(src_md, name)
            if candidate in media[repo]:
                return candidate
            name_only = unquote(name).split("|")[0].split("/")[-1].lower()
            found = lookup_media[repo].get(name_only, [])
            if len(found) == 1:
                return found[0]
            if len(found) > 1:
                # Choose nearest directory by shared path components.
                near = max(found, key=lambda p: len(set(p.parts) & set(src_md.parts)))
                warnings.append(f"Ambiguous image {name} under {repo}/{src_md}; chose {near}")
                return near
            return None

        def copy_media(repo, src):
            data = media[repo][src].read_bytes()
            digest = hashlib.sha256(data).hexdigest()
            if digest in media_sha_to_path:
                return media_sha_to_path[digest]
            dst = Path("assets/images/reference") / (digest[:20] + media[repo][src].suffix.lower())
            (BASE / dst).parent.mkdir(parents=True, exist_ok=True)
            (BASE / dst).write_bytes(data)
            media_sha_to_path[digest] = dst
            return dst

        def update_link(repo, original, dest, url):
            source, suffix = raw_link_target(original, url)
            if source is None:
                return url
            if (repo, source) in mappings:
                return relative(dest, mappings[(repo, source)]) + suffix
            if source in media[repo]:
                return relative(dest, copy_media(repo, source)) + suffix
            if source.suffix.lower() in MEDIA_SUFFIXES:
                found = find_media(repo, original, url)
                if found is not None:
                    return relative(dest, copy_media(repo, found)) + suffix
                warnings.append(f"Missing image: {repo}/{original} -> {url}")
            return url

        for repo, _ in REPOS:
            for source, content in docs[repo].items():
                dest = mappings[(repo, source)]
                if (BASE / dest).exists():
                    continue

                # Obsidian embeds ![[image name.png|width]]
                def obsidian_embed(match):
                    name = match.group(1).split("|")[0]
                    found = find_media(repo, source, name)
                    if found is None:
                        warnings.append(f"Unresolved embed: {repo}/{source} -> {name}")
                        return match.group(0)
                    return "![Captura](" + relative(dest, copy_media(repo, found)) + ")"
                content = re.sub(r"!\[\[([^\]]+)\]\]", obsidian_embed, content)

                # Standard Markdown links / images, avoiding HTTP URLs.
                def md_link(match):
                    before, link, after = match.groups()
                    stripped = link.strip()
                    if " " in stripped and not (BASE / stripped).exists():
                        # Preserve optional quoted title: URL is the initial token.
                        possible = re.match(r'^(\S+)\s+([\"\x27].+)$', stripped)
                        if possible:
                            return before + update_link(repo, source, dest, possible.group(1)) + " " + possible.group(2) + after
                    return before + update_link(repo, source, dest, stripped) + after
                content = re.sub(r"(!?\[[^\]\n]*\]\()([^\)\n]+)(\))", md_link, content)

                # Obsidian ordinary wiki-links between notes.
                def obsidian_link(match):
                    raw = match.group(1).split("|")[0].strip()
                    options = [p for p in docs[repo] if p.stem.lower() == Path(raw).stem.lower()]
                    if len(options) == 1:
                        return "[" + Path(raw).stem + "](" + relative(dest, mappings[(repo, options[0])]) + ")"
                    return match.group(0)
                content = re.sub(r"(?<!!)\[\[([^\]]+)\]\]", obsidian_link, content)

                # HTML image tags are used in some copied notes.
                content = re.sub(
                    r'(<img[^>]*\bsrc=["\x27])([^"\x27]+)(["\x27])',
                    lambda m: m.group(1) + update_link(repo, source, dest, m.group(2)) + m.group(3),
                    content, flags=re.I,
                )

                out = BASE / dest
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(content.rstrip() + "\n", encoding="utf-8")
                new_pages.add(dest)

        # Generate indexes for new topic trees, without origin-repository labels.
        for section, heading in INDEX_SECTIONS:
            prefix = Path(section)
            pages = sorted(p for p in new_pages if p != prefix / "README.md"
                           and p.parts[:len(prefix.parts)] == prefix.parts)
            if not pages:
                continue
            idx = BASE / prefix / "README.md"
            if idx.exists():  # keep any pre-existing index
                continue
            lines = [f"# {heading}", "", "Apuntes y referencias prácticas.", ""]
            for p in pages:
                lines.append(f"- [{p.stem.replace('-', ' ').title()}]({relative(prefix / 'README.md', p)})")
            lines.extend(["", "[Inicio](../../README.md)" if len(prefix.parts) == 1 else "[Inicio](../../../README.md)", ""])
            idx.parent.mkdir(parents=True, exist_ok=True)
            idx.write_text("\n".join(lines), encoding="utf-8")

        # Link new topics from the original category indexes, keeping all existing notes.
        index_links = {
            "Active-Directory/README.md": [("Técnicas avanzadas", "Advanced/README.md"), ("Notas de campo", "Field-Notes/README.md")],
            "Web-Security/README.md": [("Técnicas web", "Techniques/README.md"), ("Notas de campo", "Field-Notes/README.md"), ("CMS — referencia", "CMS/Reference/README.md")],
            "Network-Pentesting/README.md": [("Guías de enumeración de servicios", "Service-Reference/README.md")],
            "Labs-and-Writeups/README.md": [("Proving Grounds Practice", "Proving-Grounds-Practice/README.md")],
            "Methodologies/README.md": [],
        }
        for path, links in index_links.items():
            p = BASE / path
            if not p.exists():
                continue
            original = read_text(p)
            additions = [f"- [{name}]({ref})" for name, ref in links if (p.parent / ref).exists() and f"]({ref})" not in original]
            if additions:
                p.write_text(original.rstrip() + "\n\n## Referencias adicionales\n\n" + "\n".join(additions) + "\n", encoding="utf-8")
        main_readme = BASE / "README.md"
        main = read_text(main_readme)
        added = []
        for name, path, description in [
            ("Privilege Escalation", "Privilege-Escalation/README.md", "Linux y Windows: técnicas, comprobaciones y casos prácticos."),
            ("Pivoting", "Pivoting/README.md", "Tunneling, port forwarding y movimiento por redes segmentadas."),
            ("Wireless", "Wireless/README.md", "Notas de auditoría Wi-Fi."),
        ]:
            if (BASE / path).exists() and f"]({path})" not in main:
                added.append(f"| [{name}]({path}) | {description} |")
        if added:
            main += "\n## Más temas de Red Team\n\n| Tema | Contenido |\n| --- | --- |\n" + "\n".join(added) + "\n"
            main_readme.write_text(main, encoding="utf-8")

        # Remove temporary bootstrap files only once the entire integration has succeeded.
        (BASE / ".github/scripts/organize_references.py").unlink(missing_ok=True)
        (BASE / ".github/workflows/organize_references.yml").unlink(missing_ok=True)

        print(f"COMPLETED: {len(new_pages)} new Markdown pages, {len(media_sha_to_path)} total unique images indexed.")
        print(f"Warnings: {len(warnings)}")
        for w in warnings[:80]:
            print("WARNING:", w)
        if len(warnings) > 80:
            print(f"... and {len(warnings)-80} more warnings")


if __name__ == "__main__":
    main()
