<script context="module">
  export async function load({ fetch }) {
    const client_resp = await fetch("/status");
    const client_status = await client_resp.json();

    // the status depends on the backend
    const url = "/proxy/api/v1/status";
    const response = await fetch(url);

    return {
      status: response.status,
      props: {
        client_status: client_status,
        server_status: response.ok && (await response.json()),
      },
    };
  }
</script>

<script lang="ts">
  import Navbar from "$lib/Navbar.svelte";
  import { page } from "$app/stores";
  import type { ClientStatus, ServerStatus } from "$lib/interfaces";
  export let client_status: ClientStatus;
  export let server_status: ServerStatus;
</script>

<Navbar
  path={$page.url.pathname
    .split("/")
    .slice(1)
    .map((s) => s.trim())
    .filter((s) => s)}
  {client_status}
  {server_status}
/>

<slot />
