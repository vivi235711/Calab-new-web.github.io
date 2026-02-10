# Computational Astrophysics Lab (CALab) Website

Welcome to the official repository for the **Computational Astrophysics Lab (CALab)** website. This site is built with [Jekyll](https://jekyllrb.com/) and [Bootstrap 5](https://getbootstrap.com/), hosted on GitHub Pages.

---

## 📑 Table of Contents
1. [Quick Maintenance (GitHub Web Interface)](#1-quick-maintenance-github-web-interface)
   - [Update Members](#-update-members)
   - [Add/Update Research Projects](#-addupdate-research-projects)
   - [Manage Highlights & News](#-manage-highlights--news)
   - [Update Courses & Useful Links](#-update-courses--useful-links)
2. [Publications Management (Automatic)](#2-publications-management-automatic)
3. [Website Architecture](#3-website-architecture)
4. [Developer Environment & Setup](#4-developer-environment--setup)
5. [Site Standards & Guidelines](#5-site-standards--guidelines)

---

## 1. Quick Maintenance (GitHub Web Interface)

You can maintain most of the website's content without any coding knowledge by using the GitHub "Edit" (pencil icon) button.

### 👥 Update Members
Member information is stored in `_data/members.yml`.
1. Navigate to `_data/members.yml`.
2. Click the **pencil icon** to edit.
3. **Add a member**: Copy below block and update the details (name, role, position, image path, etc.).
   ```yaml
   - english_name: "Firstname Lastname"
     native_name: "姓名"
     role: "postdoc"                  # Use roles from _data/member_roles.yml
     image: "/assets/img/member/name.webp"
     website: "https://..."
     email: "user@example.com"
     github: "username"
      bio:
       - "Research interest line 1"
       - "Line 2"
     aliases: ["Lastname, F.", "Firstname L."] # Used to bold name in Publications
   ```
4. **Alumni/Previous Members**: Simply change `role` to `previous`. They will automatically move to the "Previous Members" page.
5. **Images**: Upload square (1:1) WebP images to `assets/img/member/`.

### 🚀 Add/Update Research Projects
Projects are individual Markdown files in `_projects/`.
1. **Types of Projects**:
   - **Archive Projects**: Standard research updates. Use tags like `FDM`, `GAMER_app`, or `GAMER_dev`.
   - **Main Topic Projects**: These appear on the "Research" landing page. They MUST have `tags: ["main"]` and a `modal_id`.
2. **Add New**: Create a file like `_projects/2026-new-study.md`.
3. **Template**:
   ```yaml
   ---
   title: "Study Title"
   date: 2026-02-11
   tags: ["FDM"]             # Categorizes the project
   image: "/assets/img/..."  # Thumbnail image
   link: "https://doi.org/." # External paper link
   link_text: "Journal Ref"  # Text for the link button
   ---
   Executive summary of the project...
   ```

### 🏆 Manage Highlights & News
The special "Highlights" on the News and Research Archive pages are controlled by `_data/research_section.yml`.
- Add the **filename (slug)** of a project to the corresponding list:
  ```yaml
  research_highlights:
    - project-slug-1
    - project-slug-2
  fdm_highlights:
    - project-slug-3
    - project-slug-4
  ```

### 📚 Update Courses & Useful Links
- **Courses**: Managed in `_courses/`. Edit the Markdown files to update syllabus or links.
- **Useful Links**: Managed in `_useful/`. Add new links or categories by editing the files there.

---

## 2. Publications Management (Automatic)

We use an automated pipeline to handle publications. **Do not edit `_data/publications.yml` directly!**

1. **Step**: Edit `_tools/export-bibtex.bib` and add your BibTeX entries.
2. **Automation**: A GitHub Action automatically runs `_tools/bib_to_yml.py` to:
   - Convert BibTeX to YAML.
   - Match authors against our member list (and bold them).
   - Convert LaTeX journal macros (e.g., `\apj`) to full names.
   - **Preserve Tags**: If you manually add `tags: ["FDM"]` to an entry in `_data/publications.yml`, the script will remember it even when the bib is updated (as long as the title stays the same).

---

## 3. Website Architecture

| Folder/File | Purpose |
| :--- | :--- |
| `_data/` | YAML files for Members, Publications, and Navigation. |
| `_projects/` | The core collection of research updates. |
| `_courses/` | Course materials and syllabus. |
| `_useful/` | Curated links for lab members. |
| `_includes/` | Reusable components (Navbar, Cards, Modals). |
| `_layouts/` | Page templates (Default). |
| `_sass/` | Custom styling and Bootstrap overrides. |
| `_tools/` | Tools for automatic updates. |
| `assets/` | Static assets: `img/`, `video/`, `js/`, `css/`. |
| `research/` | Page for research projects. (Entrance from research pages' modal) |
| `_config.yml` | Configuration file for Jekyll. |
| `Gemfile` | Gemfile for Jekyll. |


---

## 4. Developer Environment & Setup

### Requirements
- **Ruby 3.0+** & **Bundler**
- **Python 3.9+** (for publication script)

### Local Launch
1. `bundle install`
2. `bundle exec jekyll serve --baseurl ""`
3. Open `http://127.0.0.1:4000/`

### Deployment
Deployment is automatic! Any push to the `main` branch triggers:
1. Publication script conversion.
2. Jekyll build.
3. GitHub Pages deployment.

---

## 5. Site Standards & Guidelines

### 🖼️ Media
- **Format**: Use **WebP** for images and **WebM** for videos whenever possible for better performance.
- **Size**: Member photos should be **square** (e.g., 400x400px).
- **Video**: Laboratory/Background videos should be muted and under 10MB.

### 🏷️ Naming
- **Files**: Use `kebab-case` (e.g., `my-new-paper.md`).
- **Tags**: Stick to consistent tags: `FDM`, `GAMER_app`, `GAMER_dev`, `main`.

---

**Maintained by**: CALab Team
**Last Updated**: February 2026
