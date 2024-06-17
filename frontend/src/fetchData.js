/**
 * Fetches data from the specified URL with the provided options.
 *
 * @param {string} url - The URL to fetch data from.
 * @param {Object} [options={}] - Optional parameters for the fetch request.
 * @returns {Promise<Object>} A promise that resolves to the JSON response.
 * @throws Will log an error message if the fetch request fails.
 */
async function fetchData(url, options = {}) {
  try {
    // Fetch the response and convert it to a JavaScript Promise object.
    const response = await fetch(url, options);
    const json = await response.json();
    return json;
  } catch (error) {
    console.error("Error:", error);
  }
}

export { fetchData };

