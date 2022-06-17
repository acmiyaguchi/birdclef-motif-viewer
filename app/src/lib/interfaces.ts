interface ClientStatus {
  status: string;
  mode: string;
  version: string;
  git_sha: string;
  build_time: string;
}

interface ServerStatus {
  status: string;
  version: string;
}

interface TrackCount {
  species: string;
  count: number;
}

interface Track {
  species: string;
  name: string;
}

interface Summary {
  url: string;
}

export type { ClientStatus, ServerStatus, TrackCount, Track, Summary };
