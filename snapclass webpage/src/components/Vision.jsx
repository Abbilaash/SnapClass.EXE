import React from 'react';
import { Globe, Heart, Zap } from 'lucide-react';

const Vision = () => {
  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-6">
            Our Vision
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Making AI accessible to every student, everywhere – even without internet.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="text-center group">
            <div className="w-16 h-16 bg-gradient-to-r from-purple-600 to-purple-500 rounded-full flex items-center justify-center mx-auto mb-6 transform group-hover:scale-110 transition-transform duration-300">
              <Globe className="text-white" size={32} />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Empowering Remote Classrooms</h3>
            <p className="text-gray-600">
            Deliver AI-powered academic tools that work entirely offline, enabling equitable 
            access to intelligent education in under-connected regions.
            </p>
          </div>

          <div className="text-center group">
            <div className="w-16 h-16 bg-gradient-to-r from-purple-600 to-purple-500 rounded-full flex items-center justify-center mx-auto mb-6 transform group-hover:scale-110 transition-transform duration-300">
              <Heart className="text-white" size={32} />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Instant, Smart Feedback for Teachers</h3>
            <p className="text-gray-600">
            Equip educators with instant summaries of student learning gaps and recommended 
            actions — no internet, no delay, just insight.
            </p>
          </div>

          <div className="text-center group">
            <div className="w-16 h-16 bg-gradient-to-r from-purple-600 to-purple-500 rounded-full flex items-center justify-center mx-auto mb-6 transform group-hover:scale-110 transition-transform duration-300">
              <Zap className="text-white" size={32} />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Understanding Beyond Scores</h3>
            <p className="text-gray-600">
            Shift the focus from rote marks to real conceptual clarity by diagnosing student 
            understanding through textbooks and classroom interaction.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Vision;