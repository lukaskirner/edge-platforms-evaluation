import axios from "axios";
import { Elements } from "react-flow-renderer";
import { getAPIHost } from "../config";

export async function getReactFlowElements(): Promise<Elements | null> {
  let host = getAPIHost()
  return axios.get(host + "/api/monitor")
    .then(response => {
      console.log(response.data)
      return response.data as Elements
    })
    .catch(error => {
      console.error("An error occured", error)
      return null
    })
}
