import { useEffect, useState } from "react";

const IMAGE_ENDPOINT = "http://localhost:8000/api/grafica"; // cambia por tu endpoint

export default function Graphic() {
  const [imageUrl, setImageUrl] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchImage = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(IMAGE_ENDPOINT);
      if (!res.ok) throw new Error(`Error ${res.status}`);
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      setImageUrl((prev) => {
        if (prev) URL.revokeObjectURL(prev); // limpia la URL anterior
        return url;
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchImage();
    return () => {
      if (imageUrl) URL.revokeObjectURL(imageUrl);
    };
  }, []);

  return (
    <section className="w-full max-w-4xl mx-auto px-4 py-8">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-1 h-7 bg-nfl-red rounded-full" />
        <h2 className="text-nfl-blue text-xl font-semibold tracking-wide">
          Performance Chart
        </h2>
        <div className="flex-1 h-px bg-gray-200 ml-2" />
        <button
          onClick={fetchImage}
          className="text-nfl-blue border border-nfl-blue/30 hover:border-nfl-blue hover:bg-nfl-blue/5 transition-all px-4 py-1.5 text-xs font-semibold tracking-widest uppercase rounded-lg"
        >
          ↻ Actualizar
        </button>
      </div>

      <div className="relative w-full bg-gray-50 border border-gray-200 rounded-2xl overflow-hidden shadow-md flex items-center justify-center">
        {loading && (
          <div className="flex flex-col items-center justify-center py-24 gap-3">
            <div className="w-10 h-10 border-2 border-nfl-blue border-t-transparent rounded-full animate-spin" />
            <p className="text-gray-400 text-sm tracking-widest uppercase">Cargando gráfica...</p>
          </div>
        )}

        {error && !loading && (
          <div className="flex flex-col items-center justify-center py-24 gap-3">
            <p className="text-red-400 text-sm">{error}</p>
            <button
              onClick={fetchImage}
              className="text-nfl-blue underline text-xs"
            >
              Reintentar
            </button>
          </div>
        )}

        {imageUrl && !loading && (
          <img
            src={imageUrl}
            alt="Player performance chart"
            className="w-full h-auto block"
          />
        )}
      </div>

      <p className="text-gray-300 text-xs tracking-widest text-right mt-2 uppercase">
        * Datos en tiempo real del servidor
      </p>
    </section>
  );
}