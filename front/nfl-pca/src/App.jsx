import Header from "./components/Header";
import Graphic from "./components/Graphic";
import Form from "./components/Form";

export default function App() {
  return (
    <div className="min-h-screen bg-white text-gray-800">
      <Header />

      <main className="py-6">
        <Graphic />

        <div className="max-w-4xl mx-auto px-4 my-4">
          <div className="flex items-center gap-4">
            <div className="flex-1 h-px bg-nfl-red/30" />
            <div className="w-2 h-2 bg-nfl-red rotate-45" />
            <div className="flex-1 h-px bg-nfl-red/30" />
          </div>
        </div>

        <Form />
      </main>

      <footer className="border-t border-gray-200 py-4 text-center">
        <p className="text-gray-400 font-body text-xs tracking-widest uppercase">
          NFL Stats Dashboard © {new Date().getFullYear()}
        </p>
      </footer>
    </div>
  );
}