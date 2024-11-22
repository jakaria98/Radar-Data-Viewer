import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Footer from '../Components/Footer';
import Header from '../Components/Header';
import RadarAnimation from '../Components/RadarAnimation';

const DataViewer = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const [images, setImages] = useState([]);
    const [metadata, setMetadata] = useState({});
    const [currentIndex, setCurrentIndex] = useState(0);
    const radarData = location.state && location.state.data;
   // console.log(radarData);

    // Get data from location state
    useEffect(() => {
        if (location.state && location.state.data) {
            const { images: imgList, metadata } = location.state.data;
            setImages(imgList || []);
            setMetadata(metadata || {});
        }
    }, [location.state]);

    // Auto-slide through images
    useEffect(() => {
        if (images.length > 0) {
            const interval = setInterval(() => {
                setCurrentIndex((prevIndex) => (prevIndex + 1) % images.length);
            }, 3000); // Change image every 3 seconds
            return () => clearInterval(interval);
        }
    }, [images]);
    return (
        <>
            {!radarData ? (
                <div className="min-h-screen flex flex-col bg-black text-white relative overflow-hidden">
                    <div className="absolute inset-0 pointer-events-none flex justify-center items-center">
                        <RadarAnimation />
                    </div>

                    <Header />

                    <main className="flex-grow flex flex-col justify-center items-center py-8 relative z-10">
                        <div
                            className="w-[700px] bg-glass border-2 border-green-400 rounded-lg shadow-glass p-4"
                            style={{
                                backdropFilter: 'blur(10px)',
                                background: 'rgba(255, 255, 255, 0.1)',
                            }}
                        >
                            <div className="text-right mb-4 flex justify-end gap-2">
                                <button className="glass-button" onClick={() => navigate('/load')}>
                                    Load
                                </button>
                                <button
                                    className="glass-button"
                                    onClick={() => navigate('/upload')}
                                >
                                    Upload
                                </button>
                            </div>

                            <div
                                className="bg-glass border-2 border-green-400 rounded-lg w-full h-[400px] flex justify-center items-center"
                                style={{
                                    backdropFilter: 'blur(10px)',
                                    background: 'rgba(255, 255, 255, 0.1)',
                                }}
                            >
                                <p className="text-gray-200 text-lg">Radar Image Placeholder</p>
                            </div>

                            <div className="flex justify-center items-center mt-4 space-x-4">
                                <button className="glass-icon-button">◀️◀️</button>
                                <button className="glass-icon-button">◀️</button>
                                <button className="glass-icon-button">| |</button>
                                <button className="glass-icon-button">▶️</button>
                                <button className="glass-icon-button">▶️▶️</button>
                            </div>
                        </div>

                        <div
                            className="w-[700px] bg-glass border-2 border-green-400 rounded-lg shadow-glass p-4 mt-8"
                            style={{
                                backdropFilter: 'blur(10px)',
                                background: 'rgba(255, 255, 255, 0.1)',
                            }}
                        >
                            <h2 className="text-xl font-semibold text-green-400 mb-2">
                                Information
                            </h2>
                            <p className="text-gray-200">
                                This is a placeholder for the radar image's metadata or relevant
                                details. You can include information like date, time, radar
                                frequency, or any additional properties related to the image being
                                displayed.
                            </p>
                        </div>
                    </main>

                    <Footer />
                </div>
            ) : (
                <div className="min-h-screen flex flex-col bg-black text-white relative overflow-hidden">
                    <div className="absolute inset-0 pointer-events-none flex justify-center items-center">
                        <RadarAnimation />
                    </div>

                    <Header />

                    <main className="flex-grow flex flex-col justify-center items-center py-8 relative z-10">
                        {/* Render content based on condition */}
                        {radarData ? (
                            <>
                                <div
                                    className="w-[700px] bg-glass border-2 border-green-400 rounded-lg shadow-glass p-4"
                                    style={{
                                        backdropFilter: 'blur(10px)',
                                        background: 'rgba(255, 255, 255, 0.1)',
                                    }}
                                >
                                    <div
                                        className="bg-glass border-2 border-green-400 rounded-lg w-full h-[400px] flex justify-center items-center"
                                        style={{
                                            backdropFilter: 'blur(10px)',
                                            background: 'rgba(255, 255, 255, 0.1)',
                                        }}
                                    >
                                        {/* Display images */}
                                        {radarData.images.map((image, index) => (
                                            <img
                                                key={index}
                                                src={image}
                                                alt={`Radar ${index}`}
                                                className="max-h-full max-w-full mb-2"
                                            />
                                        ))}
                                    </div>

                                    <div className="flex justify-center items-center mt-4 space-x-4">
                                        <button className="glass-icon-button">◀️◀️</button>
                                        <button className="glass-icon-button">◀️</button>
                                        <button className="glass-icon-button">| |</button>
                                        <button className="glass-icon-button">▶️</button>
                                        <button className="glass-icon-button">▶️▶️</button>
                                    </div>
                                </div>

                                <div
                                    className="w-[700px] bg-glass border-2 border-green-400 rounded-lg shadow-glass p-4 mt-8"
                                    style={{
                                        backdropFilter: 'blur(10px)',
                                        background: 'rgba(255, 255, 255, 0.1)',
                                    }}
                                >
                                    <h2 className="text-xl font-semibold text-green-400 mb-2">
                                        Metadata Information
                                    </h2>
                                    {/* Display metadata */}
                                    <pre className="text-gray-200">
                                        {JSON.stringify(radarData.metadata, null, 2)}
                                    </pre>
                                </div>
                            </>
                        ) : (
                            <p className="text-gray-200 text-lg">
                                No data available. Please upload a file first.
                            </p>
                        )}
                    </main>

                    <Footer />
                </div>
            )}
        </>
    );
};

export default DataViewer;
