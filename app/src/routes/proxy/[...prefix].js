// ensure that all calls are made through the server, since the backend host is
// on localhost, which is not available to the browser client
export async function get({ params }) {
  const { prefix } = params;
  const url = `${import.meta.env.VITE_HOST}/${prefix}`;
  const response = await fetch(url);
  return {
    status: response.status,
    body: response.ok && (await response.json()),
  };
}
