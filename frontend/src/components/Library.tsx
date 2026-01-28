import { useQuery } from '@tanstack/react-query';
import type { Playlist } from './Playlists';

const fetchPlaylists = async (): Promise<{ playlists: Playlist[] }> => {
  const response = await fetch('/api/playlists');
  if (!response.ok) throw new Error('Failed to fetch playlists');
  return response.json();
};

export function Library() {
  const { data } = useQuery({
    queryKey: ['playlists'],
    queryFn: fetchPlaylists,
  });

  const playlists = data?.playlists || [];

  return (
    <div className="flex-1 bg-gradient-to-b from-neutral-800 to-black p-6">
      <div className="flex items-center gap-4 mb-8">
        <div className="w-8 h-8 rounded-full bg-neutral-900 flex items-center justify-center">
          <span className="text-lg">👤</span>
        </div>
        <h2 className="text-2xl font-bold">TechBase</h2> {/* Should be user.name var, ai slop...*/}
      </div>

      <div className="space-y-8">
        <section>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-bold">Your Playlists</h3>
            <button className="text-sm text-neutral-400 hover:text-white">
              Show all
            </button>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
            {playlists.slice(0, 10).map((playlist) => (
              <div
                key={playlist.id}
                className="bg-neutral-900 p-4 rounded-lg hover:bg-neutral-800 transition cursor-pointer group"
              >
                <div className="relative mb-4">
                  <img
                    src={playlist.images[0]?.url || '/placeholder.png'}
                    alt={playlist.name}
                    className="w-full aspect-square object-cover rounded-md shadow-lg"
                  />
                </div>
                <h4 className="font-semibold text-sm mb-1 truncate">
                  {playlist.name}
                </h4>
                <p className="text-xs text-neutral-400 line-clamp-2">
                  {playlist.description || `By ${playlist.owner.display_name}`} {/* After clicking the playlist, it should fetch tracks and open another page.*/}
                </p>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}
