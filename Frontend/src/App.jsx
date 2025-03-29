import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Header from './components/header'
import Navbar from './components/navbar'
import HeroSection from './components/hero'
import Rickroll from './components/pages/Rickroll'
import AboutUs from './components/pages/AboutUs'
import Tutorial from './components/pages/Tutorial'
import { SessionProvider } from './context/SessionContext'

const App = () => {
  return (
    <SessionProvider>
      <Router>
        <Header/>
        <Navbar/>
        <Routes>
          <Route path="/" element={<HeroSection/>} />
          <Route path="/rickroll" element={<Rickroll/>} />
          <Route path="/AboutUs" element={<AboutUs/>} />
          <Route path="/tutorial" element={<Tutorial/>} />
        </Routes>
      </Router>
    </SessionProvider>
  )
}

export default App
