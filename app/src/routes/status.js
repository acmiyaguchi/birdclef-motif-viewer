export async function get({ params }) {
  const { prefix } = params;
  return {
    body: {
      status: "ok",
      mode: import.meta.env.MODE,
      version: "__VERSION__",
      git_sha: "__GIT_COMMIT__",
      build_time: "__BUILD_TIME__",
    },
    status: 200,
  };
}
