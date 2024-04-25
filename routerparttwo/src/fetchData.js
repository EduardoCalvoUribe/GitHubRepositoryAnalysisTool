async function fetchData(url, options = {}) {
  try {
      // fetches response, converts to JavaScript Promise object
      const response = await fetch(url, options);
      console.log(response)
      const json = await response.json();
      return json;
  } catch (error) {
      console.error('Error:', error);
  }
}

export { fetchData };