import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async (event) => {
    const {questionId} = event.params
    const response = await fetch(
        `https://jsonplaceholder.typicode.com/posts/${questionId}`
    );
    const respondeBody = await response.json()

    return{
        body: respondeBody.body
    }
}
