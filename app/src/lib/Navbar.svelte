<script lang="ts">
  import { ClientStatus, ServerStatus } from "$lib/interfaces";
  export let path: Array<string> = [];
  export let client_status: ClientStatus;
  export let server_status: ServerStatus;
</script>

<nav class="box">
  <div>
    <a href="/">home</a>
    <span class="sep">|</span>
    <a href="/summary">summary</a>
    {#each path.filter((p) => p != "summary") as part, i}
      <span class="sep">/</span>
      <a href={"/" + path.slice(0, i + 1).join("/")}>{part}</a>
    {/each}
  </div>
  <div>
    <div>
      <b>git rev</b>:
      <a
        href="https://github.com/acmiyaguchi/birdclef-2022/commit/{client_status.git_sha}"
        >{client_status.git_sha}</a
      >
      <b>app</b>: v{client_status.version}
      <b>api</b>: v{server_status.version}
    </div>
  </div>
</nav>

<style>
  .sep {
    padding: 5px;
  }
  .box {
    display: flex;
    justify-content: space-between;
  }
</style>
