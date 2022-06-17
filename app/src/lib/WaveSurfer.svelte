<script lang="ts">
  import { onDestroy, onMount } from "svelte";
  import colormap from "colormap";

  export let audioUrl: string;
  let waveformContainer: HTMLElement;
  let spectrogramContainer: HTMLElement;
  let wavesurfer: any;

  let isPlaying: boolean = false;
  let currentTime: number = 0.0;
  let totalTime: number = 0.0;

  onMount(async () => {
    const WaveSurfer = (await import("wavesurfer.js")).default;
    const SpectrogramSurfer = (
      await import("wavesurfer.js/src/plugin/spectrogram")
    ).default;

    let spectogram = SpectrogramSurfer.create({
      wavesurfer: wavesurfer,
      container: spectrogramContainer,
      colorMap: colormap({
        colormap: "hot",
        nshades: 256,
        format: "float",
      }),
    });

    wavesurfer = WaveSurfer.create({
      container: waveformContainer,
      scrollParent: true,
      waveColor: "violet",
      progressColor: "purple",
      plugins: [spectogram],
    });

    wavesurfer.load(audioUrl);
    wavesurfer.on("ready", () => {
      totalTime = wavesurfer.getDuration().toFixed(2);
    });
    // https://stackoverflow.com/a/40638914
    wavesurfer.on("audioprocess", () => {
      currentTime = wavesurfer.getCurrentTime().toFixed(2);
    });
    wavesurfer.on("finish", () => {
      isPlaying = false;
    });
  });

  onDestroy(() => {
    // https://stackoverflow.com/questions/69605050/using-wavesurfer-js-in-a-react-app-cause-issues
    if (wavesurfer) {
      wavesurfer.destroy();
    }
  });
</script>

<button
  on:click={() => {
    wavesurfer.playPause();
    isPlaying = !isPlaying;
  }}
>
  {#if isPlaying}Pause{:else}Play{/if}
</button>
<span>{currentTime}/{totalTime}</span>
<div>
  <div id="waveform" bind:this={waveformContainer} />
  <div id="spectrogram" bind:this={spectrogramContainer} />
</div>
