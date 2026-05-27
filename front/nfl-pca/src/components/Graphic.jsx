import { useEffect, useState } from "react";

// Endpoint de ejemplo: genera una imagen aleatoria. Reemplaza con tu URL real.
const IMAGE_ENDPOINT = "https://www.imdb.com/name/nm2496281/mediaviewer/rm3533983233/";

export default function Graphic() {
  const [imageUrl, setImageUrl] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchImage = async () => {
    setLoading(true);
    setError(null);
    try {
      // Si tu endpoint devuelve JSON con una URL:
      // const res = await fetch("https://tu-endpoint.com/api/chart");
      // const data = await res.json();
      // setImageUrl(data.imageUrl);

      // Si tu endpoint devuelve la imagen directamente (blob):
      const res = await fetch(IMAGE_ENDPOINT);
      if (!res.ok) throw new Error("Error al obtener la imagen");
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      setImageUrl(url);
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
      {/* Título de sección */}
      <div className="flex items-center gap-3 mb-6">
        <div className="w-1 h-8 bg-nfl-red" />
        <h2 className="font-display text-white text-2xl tracking-widest uppercase">
          Performance Chart
        </h2>
        <div className="flex-1 h-px bg-white/10 ml-2" />
        <button
          onClick={fetchImage}
          className="text-nfl-gold border border-nfl-gold/40 hover:border-nfl-gold hover:bg-nfl-gold/10 transition-all px-4 py-1.5 text-xs font-body font-semibold tracking-widest uppercase rounded-sm"
        >
          ↻ Actualizar
        </button>
      </div>

      {/* Contenedor de imagen */}
      <div className="relative w-full aspect-video bg-nfl-gray border border-white/10 rounded overflow-hidden shadow-2xl shadow-nfl-blue/30">
        {/* Esquinas decorativas */}
        <div className="absolute top-0 left-0 w-6 h-6 border-t-2 border-l-2 border-nfl-gold z-10" />
        <div className="absolute top-0 right-0 w-6 h-6 border-t-2 border-r-2 border-nfl-gold z-10" />
        <div className="absolute bottom-0 left-0 w-6 h-6 border-b-2 border-l-2 border-nfl-gold z-10" />
        <div className="absolute bottom-0 right-0 w-6 h-6 border-b-2 border-r-2 border-nfl-gold z-10" />

        {loading && (
          <div className="absolute inset-0 flex flex-col items-center justify-center bg-nfl-dark/80">
            <div className="w-10 h-10 border-2 border-nfl-gold border-t-transparent rounded-full animate-spin mb-3" />
            <p className="text-nfl-gold font-body tracking-widest text-sm uppercase">Cargando gráfica...</p>
          </div>
        )}

        {error && (
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <p className="text-nfl-red font-body text-sm uppercase tracking-widest">{error}</p>
            <button onClick={fetchImage} className="mt-4 text-white underline text-xs">
              Reintentar
            </button>
          </div>
        )}

        {imageUrl && !loading && (
          <img
            src={imageUrl}
            alt="Player performance chart"
            className="w-full h-full object-cover"
          />
        )}
      </div>

      <p className="text-white/30 text-xs font-body tracking-widest text-right mt-2 uppercase">
        * Datos en tiempo real del servidor
      </p>
    </section>
  );
}