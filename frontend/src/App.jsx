
import { useEffect, useState } from "react";
import {
  getProjects,
  createProject,
} from "./services/api";
import "./App.css";

const STATUS_OPTIONS = {
  "To-do": ["Unknown", "Conceptualized"],
  "In progress": [
    "Make it WORK",
    "Make it RIGHT",
    "Make it FAST",
    "Github Private",
    "Updateable",
  ],
  Complete: ["GitHub Public", "File Transferred", "Junk"],
};

const PRIORITY_OPTIONS = [
  "Finished",
  "GitHubable",
  "High",
  "Medium",
  "Low",
  "Impossible",
];

const POTENTIAL_OPTIONS = [
  "Minor",
  "Major",
  "Not Mine",
  "Scalable",
  "Junk",
];

const INITIAL_FORM = {
  name: "",
  status_group: "To-do",
  status: "Unknown",
  priority: "",
  potential: "",
  next_possible_action: "",
  repository: "",
  ide: "",
  skills: "",
  last_updated: "",
};

function App() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [form, setForm] = useState(INITIAL_FORM);
  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState("");

  useEffect(() => {
    async function loadProjects() {
      try {
        const data = await getProjects();
        setProjects(data);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    }

    loadProjects();
  }, []);

  function handleChange(event) {
    const { name, value } = event.target;

    setForm((previous) => {
      if (name === "status_group") {
        return {
          ...previous,
          status_group: value,
          status: STATUS_OPTIONS[value][0],
        };
      }

      return {
        ...previous,
        [name]: value,
      };
    });
  }

  async function handleSubmit(event) {
    event.preventDefault();

    setSubmitting(true);
    setError(null);
    setSuccess("");

    const projectData = {
      name: form.name.trim() || null,
      status_group: form.status_group,
      status: form.status,
      priority: form.priority || null,
      potential: form.potential || null,
      next_possible_action:
        form.next_possible_action.trim() || null,
      repository: form.repository.trim() || null,
      ide: form.ide
        ? form.ide.split(",").map((item) => item.trim()).filter(Boolean)
        : null,
      skills: form.skills
        ? form.skills.split(",").map((item) => item.trim()).filter(Boolean)
        : null,
      last_updated: form.last_updated || null,
    };

    try {
      const newProject = await createProject(projectData);

      setProjects((previous) => [newProject, ...previous]);
      setForm(INITIAL_FORM);
      setSuccess("Project created successfully.");
    } catch (error) {
      setError(error.message);
    } finally {
      setSubmitting(false);
    }
  }

  const counts = {
    total: projects.length,
    todo: projects.filter(
      (project) => project.status_group === "To-do"
    ).length,
    inProgress: projects.filter(
      (project) => project.status_group === "In progress"
    ).length,
    complete: projects.filter(
      (project) => project.status_group === "Complete"
    ).length,
  };

  return (
    <main className="container">
      <header className="header">
        <div>
          <h1>Notion Project Dashboard</h1>
          <p>Manage and track your projects.</p>
        </div>
      </header>

      <section className="overview">
        <StatCard title="Total Projects" value={counts.total} />
        <StatCard title="To-do" value={counts.todo} />
        <StatCard title="In Progress" value={counts.inProgress} />
        <StatCard title="Complete" value={counts.complete} />
      </section>

      <section className="create-project">
        <h2>Create Project</h2>

        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <label>
              Project Name
              <input
                name="name"
                value={form.name}
                onChange={handleChange}
                maxLength={150}
                placeholder="Enter project name"
              />
            </label>

            <label>
              Status Group
              <select
                name="status_group"
                value={form.status_group}
                onChange={handleChange}
              >
                {Object.keys(STATUS_OPTIONS).map((group) => (
                  <option key={group} value={group}>
                    {group}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Status
              <select
                name="status"
                value={form.status}
                onChange={handleChange}
              >
                {STATUS_OPTIONS[form.status_group].map((status) => (
                  <option key={status} value={status}>
                    {status}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Priority
              <select
                name="priority"
                value={form.priority}
                onChange={handleChange}
              >
                <option value="">None</option>
                {PRIORITY_OPTIONS.map((priority) => (
                  <option key={priority} value={priority}>
                    {priority}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Potential
              <select
                name="potential"
                value={form.potential}
                onChange={handleChange}
              >
                <option value="">None</option>
                {POTENTIAL_OPTIONS.map((potential) => (
                  <option key={potential} value={potential}>
                    {potential}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Repository URL
              <input
                type="url"
                name="repository"
                value={form.repository}
                onChange={handleChange}
                placeholder="https://github.com/..."
              />
            </label>

            <label>
              IDE
              <input
                name="ide"
                value={form.ide}
                onChange={handleChange}
                placeholder="VSCode, PyCharm"
              />
            </label>

            <label>
              Skills
              <input
                name="skills"
                value={form.skills}
                onChange={handleChange}
                placeholder="Python, React, SQL"
              />
            </label>

            <label>
              Last Updated
              <input
                type="date"
                name="last_updated"
                value={form.last_updated}
                onChange={handleChange}
              />
            </label>

            <label className="full-width">
              Next Possible Action
              <textarea
                name="next_possible_action"
                value={form.next_possible_action}
                onChange={handleChange}
                placeholder="What should happen next?"
                rows={3}
              />
            </label>
          </div>

          <button type="submit" disabled={submitting}>
            {submitting ? "Creating..." : "Create Project"}
          </button>
        </form>

        {success && <p className="success-message">{success}</p>}
        {error && <p className="error-message">{error}</p>}
      </section>

      <section className="project-list">
        <h2>All Projects</h2>

        {loading ? (
          <p>Loading projects...</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Project</th>
                <th>Status</th>
                <th>Priority</th>
                <th>Potential</th>
                <th>IDE</th>
                <th>Skills</th>
              </tr>
            </thead>

            <tbody>
              {projects.map((project) => (
                <tr key={project.id}>
                  <td className="project-name">
                    {project.name || "Untitled project"}
                  </td>
                  <td>{project.status || "—"}</td>
                  <td>{project.priority || "—"}</td>
                  <td>{project.potential || "—"}</td>
                  <td>{project.ide?.join(", ") || "—"}</td>
                  <td>{project.skills?.join(", ") || "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </main>
  );
}

function StatCard({ title, value }) {
  return (
    <article className="stat-card">
      <p>{title}</p>
      <h2>{value}</h2>
    </article>
  );
}

export default App;
