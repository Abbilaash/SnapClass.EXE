import React from 'react';
import { Download, Sparkles } from 'lucide-react';

const Hero = () => {
  return (
    <section className="relative min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-50 via-white to-purple-100 overflow-hidden">
      {/* Background Decorations */}
      <div className="absolute inset-0">
        <div className="absolute top-20 left-10 w-72 h-72 bg-purple-200 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-pulse"></div>
        <div className="absolute top-40 right-10 w-72 h-72 bg-purple-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-pulse animation-delay-2000"></div>
        <div className="absolute -bottom-8 left-20 w-72 h-72 bg-purple-100 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-pulse animation-delay-4000"></div>
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-32">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* Left Content */}
          <div className="text-center lg:text-left">
            <div className="flex items-center justify-center lg:justify-start mb-6">
              <Sparkles className="text-purple-600 mr-2" size={24} />
              <span className="text-purple-600 font-semibold">AI-Powered Learning</span>
            </div>
            
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900 mb-6 leading-tight">
              SnapClass –{' '}
              <span className="bg-gradient-to-r from-purple-600 to-purple-500 bg-clip-text text-transparent">
                Bridge Learning Gap, Without Internet.
              </span>
            </h1>
            
            <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto lg:mx-0">
            A tool which bridges the learning gap by generating offline diagnostic tests from 
            classroom materials and analyzing student comprehension — all without needing an 
            internet connection.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
              <button className="bg-gradient-to-r from-purple-600 to-purple-500 text-white px-8 py-4 rounded-full hover:shadow-xl transform hover:scale-105 transition-all duration-300 flex items-center justify-center font-semibold text-lg">
                <Download className="mr-2" size={20} />
                Download App
              </button>
              
              <button className="border-2 border-purple-600 text-purple-600 px-8 py-4 rounded-full hover:bg-purple-600 hover:text-white transition-all duration-300 font-semibold text-lg">
                Learn More
              </button>
            </div>
          </div>

          {/* Right Illustration */}
          <div className="relative">
            <div className="relative bg-white rounded-3xl shadow-2xl p-8 transform rotate-3 hover:rotate-0 transition-transform duration-500">
              <div className="bg-gradient-to-br from-purple-100 to-purple-50 rounded-2xl p-6 mb-4">
                <div className="flex items-center mb-4">
                  <div className="w-4 h-4 bg-red-500 rounded-full mr-2"></div>
                  <div className="w-4 h-4 bg-yellow-500 rounded-full mr-2"></div>
                  <div className="w-4 h-4 bg-green-500 rounded-full"></div>
                </div>
                <div className="bg-white rounded-lg p-4 mb-4 shadow-sm">
                  <div className="flex items-center mb-2">
                    <div className="w-8 h-8 bg-purple-600 rounded-full flex items-center justify-center mr-3">
                      <span className="text-white text-sm font-bold">📸</span>
                    </div>
                    <span className="font-semibold text-gray-800">Create test</span>
                  </div>
                  <div className="bg-gray-100 rounded p-2 text-sm text-gray-600 mb-2">
                    "Unit 2: Human Circulatory System"
                  </div>
                  <div className="bg-purple-50 rounded p-3 text-sm">
                    <p className="text-purple-800 font-medium">AI Evaluation:</p>
                    <p className="text-gray-700 mt-1">This topic shows varied understanding among students. Conceptual gaps found in blood flow, valves, and oxygenation…</p>
                  </div>
                </div>
                <div className="flex items-center justify-between text-sm text-gray-500">
                  <span>🚫 No Internet Required</span>
                  <span>⚡ Smart Evaluation</span>
                </div>
              </div>
            </div>
            
            {/* Floating Elements */}
            <div className="absolute -top-4 -right-4 bg-purple-600 text-white p-3 rounded-full shadow-lg animate-bounce">
              🧠
            </div>
            <div className="absolute -bottom-4 -left-4 bg-white text-purple-600 p-3 rounded-full shadow-lg animate-pulse">
              📚
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;