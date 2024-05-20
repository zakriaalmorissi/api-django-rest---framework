import axios from 'axios';
import React from 'react';
import { useState, useEffect } from 'react';
import './styles/App.css';

const Api = () => {
    const [posts, setPosts] = useState([]);
    const [comment, setComment] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const postId = e.target.getAttribute('data-post-id');
            console.log(postId)
            const res = await axios.post(`http://127.0.0.1:8000/posts-actions/${postId}/comment/`, { content: comment });
            if (res.status === 201) {
                alert("Comment added");
                setComment(""); // Clear the comment input after successful submission
            } else {
                console.log(res.status)
                alert("Failed to add comment");
            }
        } catch (error) {
            console.error("Error:", error);
        }
    };

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/posts/')
            .then(response => {
                setPosts(response.data);
            })
            .catch(error => {
                console.error("Failed to fetch posts:", error);
            });
    }, []);

    return (
        <main>
            <section className='section-one'>
                Section One
            </section>
            <section className='section-two'>
                <div>
                    {posts.map(post => (
                        <div key={post.id} className='post'>
                            <div className='post-contents'> 
                                <p>{post.author}</p>
                                <p>{post.content}</p>
                            </div>
                
                            <div className='comments'>
                                {post.comments.map(comment => (
                                    <div className='comments-contents' key={comment.id}>
                                        <p>{comment.author}</p>
                                        <p>{comment.content}</p>
                                    </div>
                                ))}
                                <div className='comment-form'>
                                    <form onSubmit={handleSubmit} data-post-id={post.id}>
                                        <input
                                            type='text'
                                            placeholder='Write a comment'
                                            value={comment}
                                            onChange={(e) => setComment(e.target.value)}
                                        />
                                        <button type='submit'> Send </button>
                                    </form>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </section>
            <section className='section-three'>
                Section Three
            </section>
        </main>
    );
}

export default Api;
