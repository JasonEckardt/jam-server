import { Button } from "@/components/ui/button";

const NotFoundPage = () => {
  return <div className="flex min-h-screen flex-col items-center justify-center bg-black text-white px-4">
    <div className="text-center space-y-6 max-w-md">
      {/* Logo */}
      <div className="flex flex-col items-center gap-4">
        <div className="bg-black p-8 rounded-lg">
          <svg
            width="100"
            height="100"
            viewBox="0 0 100 100"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            {/* Vinyl record outer circle */}
            <circle cx="50" cy="50" r="48" fill="#22c55e" opacity="0.15" />
            {/* Vinyl grooves */}
            <circle cx="50" cy="50" r="42" fill="none" stroke="#22c55e" strokeWidth="1" opacity="0.3" />
            <circle cx="50" cy="50" r="36" fill="none" stroke="#22c55e" strokeWidth="1" opacity="0.3" />
            <circle cx="50" cy="50" r="30" fill="none" stroke="#22c55e" strokeWidth="1" opacity="0.3" />
            {/* Center label */}
            <circle cx="50" cy="50" r="20" fill="#22c55e" opacity="0.9" />
            <circle cx="50" cy="50" r="6" fill="black" />
          </svg>
        </div>
      </div>

      <h1 className="text-5xl font-bold">Page not found</h1>

      <p className="text-lg text-neutral-400">
        We can't seem to find the page you are looking for.
      </p>

      <Button
        asChild
        className="bg-white text-black hover:bg-gray-200 hover:scale-105 transition-transform mt-8 px-8 py-6 text-base font-semibold rounded-full"
      >
        <a href="/">Home</a>
      </Button>
    </div>
  </div>;
};

export default NotFoundPage;
