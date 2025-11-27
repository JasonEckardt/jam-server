import { Library } from "@/components/Library";
import { Playlists } from "@/components/Playlists";
import useUser from "@/hooks/useUser";

const LibraryPage = () => {
  const { } = useUser();

  return (
    <div className="flex h-screen bg-black text-white">
      <div className="hidden md:block">
        <Playlists />
      </div>
      <Library />
    </div>
  )
};

export default LibraryPage;
