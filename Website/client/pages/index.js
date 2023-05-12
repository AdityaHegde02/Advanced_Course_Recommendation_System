import Image from 'next/image'
import { Inter } from 'next/font/google'
import { useEffect, useState } from 'react'
import Navbar from '@/components/navbar'
import Hero from '@/components/hero'
import Footer from '@/components/footer'


export default function Home() {

  const [courseList,setCourseList] = useState([])
  const [input,setInput] = useState("")

  function fetchTopCourses(){
    fetch(`http://127.0.0.1:5000/predict?desc=${input}`)
    .then(res=>res.json())
    .then(data=>{
      if(data.status=='ok'){
        let uniqueArr = data.data.filter((obj, index, self) => {
          return index === self.findIndex((t) => (
            t[0] === obj[0]
          ));
        });
        console.log("uniq: ",uniqueArr)
        setCourseList(uniqueArr.slice(0,10))
      }
    })
    .catch((err)=>{
      console.log(err)
    })
  }


  // setCourseList(["Hello there"])

  return (
    <main className="flex flex-col items-center justify-center">

      <Navbar />
      <Hero />

      <h1 className='text-3xl font-bold mb-6'>Enter Course Description</h1>

      <div className= 'flex gap-6 mb-10'>
        <input className='' placeholder='Enter here' value={input} onChange={e=>setInput(e.target.value)} />
        <button onClick={fetchTopCourses}>Submit</button>
      </div>

      <ol>
        {
          courseList.map((el,idx)=>(
            <li>
             <a href={el[1]} target='_blank' className='w-full'>{idx+1}. {el[0]}</a>
            </li>
          ))
        }
      </ol>

      <Footer />

    </main>
  )
}
