
import { useEffect, useState } from "react";
import { getProjects } from "./services/api";
import "./App.css";

function App() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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

  if (loading) {
    return <main className="container">Loading dashboard...</main>;
  }

  if (error) {
    return <main className="container">Error: {error}</main>;
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

      <section className="project-list">
        <h2>All Projects</h2>

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
