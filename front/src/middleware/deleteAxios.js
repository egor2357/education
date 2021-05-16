export default async (axios, url, payload) => {
  try {
      let res = await axios.delete(url, {data: payload});
      return res
    } catch (e) {
      if (e.response) {
        return e.response
      } else {
        return e
      }
    }
}
