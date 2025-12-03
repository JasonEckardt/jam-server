import { useQuery } from '@tanstack/react-query';
import { Search, Plus, List } from 'lucide-react';
import { useState } from 'react';

interface PlaylistImage {
  height: number | null;
  url: string;
  width: number | null;
}

interface PlaylistOwner {
  display_name: string;
  external_urls: {
    spotify: string;
  };
  href: string;
  id: string;
  type: string;
  uri: string;
}

export interface Playlist {
  description: string;
  id: string;
  images: PlaylistImage[];
  link: string;
  name: string;
  owner: PlaylistOwner;
  track_count: number;
}

const fetchPlaylists = async () => {
  const response = await fetch('/api/playlists');
  if (!response.ok) throw new Error('Failed to fetch playlists');
  return response.json();
};

export function Playlists() {
  const [filter, setFilter] = useState('Playlists');
  const { data, isLoading, isError } = useQuery({
    queryKey: ['playlists'],
    queryFn: fetchPlaylists,
  });

  const playlists = data?.playlists || [];

  return (
    <div className="flex h-screen bg-black text-white">
      {/* Left Sidebar */}
      <div className="w-80 bg-neutral-900 flex flex-col">
        {/* Header */}
        <div className="p-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <svg className="w-6 h-6" viewBox="0 0 24 24" fill="currentColor">
              <path d="M3 22a1 1 0 0 1-1-1V3a1 1 0 0 1 2 0v18a1 1 0 0 1-1 1zM15.5 2.134A1 1 0 0 0 14 3v18a1 1 0 0 0 1.5.866l8-4.5a1 1 0 0 0 0-1.732l-8-4.5a1 1 0 0 0-1.5.866z" />
            </svg>
            <h1 className="text-base font-semibold">Your Library</h1>
          </div>
          <div className="flex gap-2">
            <button className="p-2 hover:bg-neutral-800 rounded-full transition">
              <Plus className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Filter Tabs */}
        <div className="px-4 flex gap-2 mb-2">
          {['Playlists', 'Podcasts', 'Albums'].map((tab) => (
            <button
              key={tab}
              onClick={() => setFilter(tab)}
              className={`px-3 py-1.5 rounded-full text-sm transition ${filter === tab
                ? 'bg-white text-black'
                : 'bg-neutral-800 hover:bg-neutral-700'
                }`}
            >
              {tab}
            </button>
          ))}
        </div>

        {/* Search and Sort */}
        <div className="px-4 mb-2 flex items-center justify-between">
          <button className="p-2 hover:bg-neutral-800 rounded-full transition">
            <Search className="w-5 h-5" />
          </button>
          <button className="flex items-center gap-2 text-sm hover:text-white transition">
            <span>Recents</span>
            <List className="w-4 h-4" />
          </button>
        </div>

        {/* Playlists List */}
        <div className="flex-1 overflow-y-auto px-2">
          {isLoading && (
            <div className="p-4 text-center text-neutral-400">Loading...</div>
          )}

          {isError && (
            <div className="p-4 text-center text-red-400">Failed to load playlists</div>
          )}

          {playlists.map((playlist: Playlist) => (
            <div
              key={playlist.id}
              className="flex gap-3 p-2 rounded-md hover:bg-neutral-800 cursor-pointer transition group"
            >
              {/* Playlist Image */}
              <img
                src={playlist.images[0]?.url || '/placeholder.png'}
                alt={playlist.name}
                className="w-12 h-12 rounded object-cover flex-shrink-0"
              />

              {/* Playlist Info */}
              <div className="flex-1 min-w-0">
                <h3 className="font-semibold text-sm truncate group-hover:text-white">
                  {playlist.name}
                </h3>
                <p className="text-xs text-neutral-400 truncate">
                  Playlist • {playlist.owner.display_name}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
