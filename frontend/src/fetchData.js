async function fetchData(url) {
    try {
      // fetches response, converts to JavaScript Promise object
      const response = await fetch(url)
      const json = await response.json() 
      return json
    } catch (error) {
      console.error('Error:', error)
    }   
  }

  export { fetchData };