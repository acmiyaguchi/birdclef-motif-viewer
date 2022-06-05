<script context="module">
  export async function load({ fetch }) {
    const url = "/proxy/api/v1/status";
    const response = await fetch(url);

    return {
      status: response.status,
      props: {
        server_status: response.ok && (await response.json()),
      },
    };
  }
</script>

<script lang="ts">
  import type { ServerStatus } from "$lib/interfaces";
  export let server_status: ServerStatus;
</script>

<nav>
  <a href="/">Home</a>
  <span>backend version: {server_status.version}</span>
</nav>

<slot />
