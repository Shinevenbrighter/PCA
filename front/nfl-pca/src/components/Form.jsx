import { useState } from "react";

const API_URL = "http://localhost:3000/api/players";

const FIELDS = [
  { name: "nombre ",   label: "Nombre del Jugador", type: "text",   placeholder: "Ej. Patrick Mahomes" },
  { name: "velocidad",        label: "Velocidad",           type: "number", placeholder: "0 – 100" },
  { name: "agilidad",      label: "Agilidad",            type: "number", placeholder: "0 – 100" },
  { name: "fuerza",     label: "Fuerza",              type: "number", placeholder: "0 – 100" },
  { name: "potencia",        label: "Potencia",            type: "number", placeholder: "0 – 100" },
  { name: "edad",          label: "Edad",                type: "number", placeholder: "Años" },
  { name: "peso",       label: "Peso (kg)",           type: "number", placeholder: "kg" },
  { name: "altura",       label: "Altura (cm)",         type: "number", placeholder: "cm" },
  { name: "partidos_jugados",  label: "Partidos Jugados",    type: "number", placeholder: "Total" },
  { name: "puntos_anotados", label: "Puntos Anotados",     type: "number", placeholder: "Total" },
  { name: "partidos_ganados",     label: "Partidos Ganados",    type: "number", placeholder: "Total" },
];

const initialState = Object.fromEntries(FIELDS.map((f) => [f.name, ""]));

export default function Form() {
  const [formData, setFormData] = useState(initialState);
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!res.ok) throw new Error(`Error ${res.status}`);

      setSubmitted(true);
      setFormData(initialState);
      setTimeout(() => setSubmitted(false), 3000);
    } catch (err) {
      setError(`No se pudo registrar el jugador: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFormData(initialState);
    setError(null);
  };

  return (
    <section className="w-full max-w-4xl mx-auto px-4 pb-12">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-1 h-7 bg-nfl-gold rounded-full" />
        <h2 className="text-nfl-blue text-xl font-semibold tracking-wide">
          Registro de Jugador
        </h2>
        <div className="flex-1 h-px bg-gray-200 ml-2" />
      </div>

      <form
        onSubmit={handleSubmit}
        className="bg-white border border-gray-200 rounded-2xl p-6 shadow-md relative overflow-hidden"
      >
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5 relative z-10">
          {FIELDS.map((field) => (
            <div key={field.name} className="flex flex-col gap-1.5">
              <label
                htmlFor={field.name}
                className="text-gray-500 text-xs font-medium tracking-wide uppercase"
              >
                {field.label}
              </label>
              <input
                id={field.name}
                name={field.name}
                type={field.type}
                placeholder={field.placeholder}
                value={formData[field.name]}
                onChange={handleChange}
                required
                className="bg-gray-50 border border-gray-200 focus:border-nfl-blue focus:ring-2 focus:ring-nfl-blue/10 focus:outline-none rounded-xl px-4 py-2.5 text-gray-700 text-sm placeholder-gray-300 transition-all"
              />
            </div>
          ))}
        </div>

        <div className="flex flex-col sm:flex-row gap-3 mt-8 relative z-10">
          <button
            type="submit"
            disabled={loading}
            className="flex-1 bg-nfl-blue hover:bg-blue-900 disabled:opacity-60 disabled:cursor-not-allowed transition-colors text-white font-semibold py-3 px-6 rounded-xl shadow-sm text-sm tracking-wide"
          >
            {loading ? "Enviando..." : "Registrar Jugador"}
          </button>
          <button
            type="button"
            onClick={handleReset}
            className="sm:w-40 border border-gray-200 hover:border-gray-400 transition-colors text-gray-400 hover:text-gray-600 font-medium py-3 px-6 rounded-xl text-sm tracking-wide"
          >
            Limpiar
          </button>
        </div>

        {submitted && (
          <div className="mt-4 border border-green-200 bg-green-50 rounded-xl px-4 py-3 text-green-600 text-sm text-center">
            ✓ Jugador registrado correctamente
          </div>
        )}

        {error && (
          <div className="mt-4 border border-red-200 bg-red-50 rounded-xl px-4 py-3 text-red-500 text-sm text-center">
            ✗ {error}
          </div>
        )}
      </form>
    </section>
  );
}