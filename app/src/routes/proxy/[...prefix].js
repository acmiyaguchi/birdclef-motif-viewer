// ensure that all calls are made through the server, since the backend host is
// on localhost, which is not available to the browser client
export async function get({ params, url }) {
  const { prefix } = params;
  const query = new URLSearchParams(url.searchParams);
  return await fetch(`${import.meta.env.VITE_HOST}/${prefix}?${query}`);
}
