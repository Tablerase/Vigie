export default class APIService {
    static UpdateArticle(id, content) {
        return fetch(`http://localhost:5000/update/${id}/`, {
            'method': 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            content: JSON.stringify(content)
        })
        .then(resp => resp.json()) 
    }
}