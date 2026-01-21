"use client";

import { useState, useEffect } from "react";
import { Trash2, Edit2, Save, Plus, Cat, DollarSign } from "lucide-react";

// --- TYPES ---
interface Cat {
  id: number;
  name: string;
  years_of_experience: number;
  breed: string;
  salary: number;
}

export default function SpyCatDashboard() {
  const [cats, setCats] = useState<Cat[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Form State
  const [newName, setNewName] = useState("");
  const [newBreed, setNewBreed] = useState("");
  const [newExperience, setNewExperience] = useState("");
  const [newSalary, setNewSalary] = useState("");

  // Edit State
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editSalary, setEditSalary] = useState<string>("");

  const API_URL = "http://127.0.0.1:8000/cats";

  // --- FETCH CATS ---
  const fetchCats = async () => {
    try {
      const res = await fetch(API_URL + "/");
      if (!res.ok) throw new Error("Failed to fetch data");
      const data = await res.json();
      setCats(data);
    } catch (err) {
      console.error(err);
      setError("Could not load cats. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCats();
  }, []);

  // --- ADD CAT ---
  const handleAddCat = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    const catData = {
      name: newName,
      breed: newBreed,
      years_of_experience: parseInt(newExperience),
      salary: parseFloat(newSalary),
    };

    try {
      const res = await fetch(API_URL + "/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(catData),
      });

      if (!res.ok) {
        // Handle validation error (e.g. invalid breed)
        const errData = await res.json();
        throw new Error(errData.detail || "Failed to create cat");
      }

      const createdCat = await res.json();
      setCats([...cats, createdCat]); // Update UI instantly

      // Reset Form
      setNewName("");
      setNewBreed("");
      setNewExperience("");
      setNewSalary("");
    } catch (err: any) {
      setError(err.message);
    }
  };

  // --- DELETE CAT ---
  const handleDelete = async (id: number) => {
    if (!confirm("Are you sure you want to remove this agent?")) return;

    try {
      const res = await fetch(`${API_URL}/${id}`, { method: "DELETE" });
      if (res.ok) {
        setCats(cats.filter((cat) => cat.id !== id));
      }
    } catch (err) {
      console.error(err);
      alert("Failed to delete");
    }
  };

  // --- UPDATE SALARY ---
  const startEditing = (cat: Cat) => {
    setEditingId(cat.id);
    setEditSalary(cat.salary.toString());
  };

  const saveSalary = async (id: number) => {
    try {
      const res = await fetch(`${API_URL}/${id}/salary?salary=${editSalary}`, {
        method: "PUT",
      });

      if (res.ok) {
        setCats(
          cats.map((cat) =>
            cat.id === id ? { ...cat, salary: parseFloat(editSalary) } : cat
          )
        );
        setEditingId(null);
      } else {
        alert("Failed to update salary");
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8 font-sans">
      <div className="max-w-5xl mx-auto">
        {/* HEADER */}
        <div className="flex items-center gap-3 mb-8">
          <div className="p-3 bg-indigo-600 rounded-lg shadow-lg">
            <Cat className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-gray-800">
            Spy Cat Agency <span className="text-indigo-600">Dashboard</span>
          </h1>
        </div>

        {/* ERROR MESSAGE */}
        {error && (
          <div className="mb-6 p-4 bg-red-100 text-red-700 border-l-4 border-red-500 rounded">
            <strong>Error:</strong> {error}
          </div>
        )}

        {/* ADD CAT FORM */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 mb-8">
          <h2 className="text-lg font-semibold text-gray-700 mb-4 flex items-center gap-2">
            <Plus className="w-5 h-5" /> Recruit New Agent
          </h2>
          <form onSubmit={handleAddCat} className="grid grid-cols-1 md:grid-cols-5 gap-4">
            <input
              type="text"
              placeholder="Code Name"
              value={newName}
              onChange={(e) => setNewName(e.target.value)}
              className="p-2 border rounded focus:ring-2 focus:ring-indigo-500 outline-none text-black"
              required
            />
            <input
              type="text"
              placeholder="Breed (e.g. Siberian)"
              value={newBreed}
              onChange={(e) => setNewBreed(e.target.value)}
              className="p-2 border rounded focus:ring-2 focus:ring-indigo-500 outline-none text-black"
              required
            />
            <input
              type="number"
              placeholder="Years Exp."
              value={newExperience}
              onChange={(e) => setNewExperience(e.target.value)}
              className="p-2 border rounded focus:ring-2 focus:ring-indigo-500 outline-none text-black"
              required
            />
            <input
              type="number"
              placeholder="Salary ($)"
              value={newSalary}
              onChange={(e) => setNewSalary(e.target.value)}
              className="p-2 border rounded focus:ring-2 focus:ring-indigo-500 outline-none text-black"
              required
            />
            <button
              type="submit"
              className="bg-indigo-600 text-white font-medium py-2 px-4 rounded hover:bg-indigo-700 transition"
            >
              Recruit
            </button>
          </form>
        </div>

        {/* CAT LIST */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
          <table className="w-full text-left">
            <thead className="bg-gray-50 border-b">
              <tr>
                <th className="p-4 font-semibold text-gray-600">Agent Name</th>
                <th className="p-4 font-semibold text-gray-600">Breed</th>
                <th className="p-4 font-semibold text-gray-600">Experience</th>
                <th className="p-4 font-semibold text-gray-600">Salary</th>
                <th className="p-4 font-semibold text-gray-600 text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan={5} className="p-8 text-center text-gray-500">
                    Loading agents...
                  </td>
                </tr>
              ) : cats.length === 0 ? (
                <tr>
                  <td colSpan={5} className="p-8 text-center text-gray-500">
                    No agents found. Recruit one above!
                  </td>
                </tr>
              ) : (
                cats.map((cat) => (
                  <tr key={cat.id} className="border-b last:border-0 hover:bg-gray-50 transition">
                    <td className="p-4 font-medium text-gray-800">{cat.name}</td>
                    <td className="p-4 text-gray-600">
                      <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">
                        {cat.breed}
                      </span>
                    </td>
                    <td className="p-4 text-gray-600">{cat.years_of_experience} years</td>

                    {/* EDITABLE SALARY COLUMN */}
                    <td className="p-4 text-gray-600">
                      {editingId === cat.id ? (
                        <div className="flex items-center gap-2">
                          <input
                            type="number"
                            value={editSalary}
                            onChange={(e) => setEditSalary(e.target.value)}
                            className="w-24 p-1 border rounded text-black"
                            autoFocus
                          />
                        </div>
                      ) : (
                        <div className="flex items-center gap-1">
                          <DollarSign className="w-4 h-4 text-green-600" />
                          {cat.salary.toLocaleString()}
                        </div>
                      )}
                    </td>

                    {/* ACTIONS COLUMN */}
                    <td className="p-4 text-right">
                      {editingId === cat.id ? (
                        <button
                          onClick={() => saveSalary(cat.id)}
                          className="text-green-600 hover:text-green-800 mr-4 font-medium"
                        >
                          <Save className="w-5 h-5 inline" /> Save
                        </button>
                      ) : (
                        <button
                          onClick={() => startEditing(cat)}
                          className="text-gray-400 hover:text-indigo-600 mr-4 transition"
                          title="Edit Salary"
                        >
                          <Edit2 className="w-5 h-5" />
                        </button>
                      )}

                      <button
                        onClick={() => handleDelete(cat.id)}
                        className="text-gray-400 hover:text-red-600 transition"
                        title="Retire Agent"
                      >
                        <Trash2 className="w-5 h-5" />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}