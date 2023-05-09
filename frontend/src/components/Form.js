import React, { useEffect, useState } from 'react'
import APIService from '../components/APIService';

function Form(props) {
    const[title, setTitle] = useState('')
    const[content, setContent] = useState('')

    useEffect(() => {
        setTitle(props.article.title)
        setContent(props.article.content)
    }, [props.article])

    const updateArticle = () => {
        APIService.UpdateArticle(props.article.id, { title, content })
            .then(resp => props.updatedData(resp))
            .catch(error => console.log(error))
    }

    return (
    <div>
        {props.article ? 
            (
            <div className='mb-3'>
                <label htmlFor = 'title' className='form-label'>Title</label>
                <input type='text' className='form-control' value={title} placeholder='Please Enter Title' onChange = {(e) => setTitle(e.target.value)} />
                <label htmlFor = 'content' className='form-label'>Content</label>
                <textarea  rows= '5' className='form-control' value={content} placeholder='Please Enter Content' onChange = {(e) => setContent(e.target.value)}/>
                <button className='btn btn-success mt-3' onClick={updateArticle}>Update</button>
            </div>
            )
            :null
        }
    </div>)
}

export default Form