# Computational Astrophysics Lab (CALab) Website

Welcome to the official repository for the **Computational Astrophysics Lab (CALab)** website. This site is built using [Jekyll](https://jekyllrb.com/) and is hosted on GitHub Pages. It serves as a hub for our research projects, publications, team members, and academic activities.

---

## 1. Quick Start Maintenance Guide (GitHub Web Interface)

You don't need to be a developer to update most of the website's content. You can make changes directly through the GitHub website using the "Edit" (pencil icon) button.

### 👥 Update Members
Member information is stored in `_data/members.yml`.
1. Navigate to `_data/members.yml`.
2. Click the **pencil icon** to edit.
3. **Add a member**: Copy an existing block and update the details (name, role, position, image path, etc.).
4. **Remove a member**: Delete their corresponding block.
5. **Change role**: Update the `role` field (e.g., `postdoc`, `master`, `previous`).
6. Scroll down, write a brief commit message, and click **Commit changes**.

### 🚀 Add Research Projects
Projects are individual Markdown files in the `_projects/` directory.
1. Navigate to `_projects/`.
2. Click **Add file** > **Create new file**.
3. Name it using a slug format (e.g., `new-project-2026.md`).
4. **Required Front Matter**: Every project MUST start with a block like this:
   ```yaml
   ---
   title: "Project Title"
   tags: ["FDM"]             # Use "FDM", "GAMER_app", or "GAMER_dev"
   image: "/assets/img/your-image.webp"
   date: 2026-01-29
   # For main research topics only (e.g., FDM.md):
   # modal_id: FDM
   # research_url: /research/fdm/
   # sort_order: 1
   ---
   Project description goes here...
   ```
5. Click **Commit changes**.

### 📚 Update Publications
Publications are managed in `_data/publications.yml`.
- **Manual Update**: Edit the file directly in GitHub, following the existing YAML structure.
- **Developer Update**: If you have a `.bib` file, you can use the script in `_tools/bib_to_yml.py` (requires local environment).

### 🚀 Pushing Changes
When you commit changes directly to the `main` branch on GitHub, a **GitHub Action** will automatically trigger, rebuilding the site and deploying it within 1-2 minutes.

---

## 2. Full Website Architecture

The site is built with **Jekyll**, a static site generator, and styled with **Bootstrap 5**.

### Directory Structure

| Folder | Purpose |
| :--- | :--- |
| `_data/` | Global data files (members, publications, navigation, etc.). |
| `_projects/` | The core content collection. Driven by tags for categorization. |
| `_includes/` | Reusable HTML snippets (headers, footers, cards, modals). |
| `_layouts/` | Base page templates (e.g., `default.html`). |
| `_sass/` | Custom SASS styles and Bootstrap overrides. |
| `_tools/` | Auxiliary scripts (e.g., BibTeX to YAML converter). |
| `assets/` | Static files: `img/` (images), `video/` (intro clips), `css/`, `js/`. |
| `research/` | Specific landing pages and archives for research directions. |

### Data Logic
- **`site.data.*`**: Jekyll automatically parses YAML files in `_data/`. For example, `site.data.members` accesses the list in `members.yml`.
- **Collections**: `_projects` is a collection. We use `jekyll-paginate-v2` to create filtered archive pages for FDM, GAMER, etc., based on project tags.

---

## 3. Developer Environment Setup

To run the website locally for testing or major design changes:

### Requirements
- **Ruby** (v3.0+)
- **Bundler** (`gem install bundler`)
- **Jekyll**

### Local Setup & Launch
1. Clone the repository:
   ```bash
   git clone https://github.com/vivi235711/Calab-new-web.github.io.git
   cd Calab-new-web.github.io
   ```
2. Install dependencies:
   ```bash
   bundle install
   ```
3. Run the development server:
   ```bash
   bundle exec jekyll serve --baseurl ""
   ```
4. Open your browser at: `http://127.0.0.1:4000/`

### Troubleshooting
- **Dependency Errors**: If `bundle install` fails, try running `bundle update` or deleting `Gemfile.lock` and reinstalling.
- **Port Busy**: If 4000 is taken, use `bundle exec jekyll serve --port 4001`.
- **Clean Cache**: If changes aren't showing up, run `bundle exec jekyll clean`.

---

## 4. Site Rules & Standards

### 🖼️ Image Standards
- **Location**: Always upload images to `assets/img/`. Subfolders like `assets/img/member/` are encouraged.
- **Format**: **WebP** is the preferred format for the web (smaller, faster). JPG/PNG are acceptable but should be optimized.
- **Consistency**: 
    - **Member Photos**: Should ideally be square (e.g., 400x400px).
    - **Project Thumbnails**: Use a consistent aspect ratio (e.g., 4:3 or 16:9).

### 🏷️ Naming Conventions
- **Collections/Files**: Use `kebab-case` (e.g., `fuzzy-dark-matter-study.md`).
- **Styles**: Follow BEM or standard Bootstrap utility patterns.

### 🎨 CSS & Styling
- **Bootstrap 5**: Use Bootstrap's built-in utility classes (e.g., `mt-5`, `d-flex`, `text-center`) whenever possible.
- **Custom SASS**: Add custom logic to `_sass/custom/`. Do not modify the core Bootstrap files directly.

---

## 5. Features Overview

- **Featured Research**: Controlled via `_data/research_section.yml`. You can pin specific projects to the top of archives.
- **Interactive Modals**: Projects on the Research landing page open detailed modals defined in `_projects/`.
- **Publication Filtering**: The publications page includes a JS-based filter to sort by year or topic.
- **Responsive Design**: Built with a mobile-first approach using Bootstrap 5's responsive grid.
- **MathJax Support**: Enabled for rendering mathematical equations in project descriptions.

---

**Maintained by**: CA Lab Team
**Last Overhaul**: January 2026
