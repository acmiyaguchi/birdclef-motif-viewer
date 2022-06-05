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

export type { ServerStatus, TrackCount, Track, Summary };
