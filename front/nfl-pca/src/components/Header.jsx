export default function Header() {
  return (
    <header className="w-full bg-nfl-blue border-b-4 border-nfl-red shadow-lg shadow-nfl-red/20">
      <div className="max-w-6xl mx-auto px-6 py-4 flex items-center gap-4">

        {/* Tu logo aquí — pon la imagen en /public/logo.png */}
        <img
          src="/logo.png"
          alt="NFL Logo"
          className="h-14 w-auto object-contain"
        />

        <div>
          <h1 className="font-display text-white text-3xl tracking-wider uppercase leading-none">
            NFL-PCA
          </h1>
          <p className="text-nfl-gold font-body text-sm tracking-[0.3em] uppercase mt-0.5">
            Model trainnig
          </p>
        </div>

        <div className="ml-auto hidden sm:flex items-center gap-2 opacity-40">
          <div className="w-16 h-px bg-nfl-gold" />
          <div className="w-2 h-2 rounded-full bg-nfl-gold" />
          <div className="w-8 h-px bg-nfl-gold" />
        </div>
      </div>
    </header>
  );
}