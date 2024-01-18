import Post from "~/components/post"
import {posts} from "../../../mock/posts"

const ForYou = () => {
  return (
    <>
    { posts.map(post => <Post post = {post} key={post.id}/> )}
    </>
  )
}

export default ForYou