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
    const [isPlaying, setIsPlaying] = useState(true); // State to control play/pause
    const radarData = location.state && location.state.data;

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
        let interval;
        if (images.length > 0 && isPlaying) {
            interval = setInterval(() => {
                setCurrentIndex((prevIndex) => (prevIndex + 1) % images.length);
            }, 3000); // Change image every 3 seconds
        }
        return () => clearInterval(interval);
    }, [images, isPlaying]);

    // Navigate to previous and next images
    const handlePrevImage = () => {
        setCurrentIndex((prevIndex) => (prevIndex - 1 + images.length) % images.length);
    };

    const handleNextImage = () => {
        setCurrentIndex((prevIndex) => (prevIndex + 1) % images.length);
    };

    const handleFirstImage = () => {
        setCurrentIndex(0);
    };

    const handleLastImage = () => {
        setCurrentIndex(images.length - 1);
    };

    const togglePlayPause = () => {
        setIsPlaying(!isPlaying);
    };

    return (
        <>
            {!radarData ? (
                <div className="min-h-screen flex flex-col bg-black text-white relative overflow-hidden">
                    <div className="absolute inset-0 pointer-events-none flex justify-center items-center">
                        <RadarAnimation />
                    </div>

                    <Header />

                    <main className="flex-grow flex flex-col justify-center items-center py-8 relative z-10">
                        <div className="w-[700px] bg-glass border-2 border-green-400 rounded-lg shadow-glass p-4">
                            <p className="text-gray-200 text-lg">
                                No data available. Please upload a file first.
                            </p>
                            <div className="text-right mb-4 flex justify-end gap-2">
                                <button
                                    className="glass-button"
                                    onClick={() => navigate('/upload')}
                                >
                                    Upload
                                </button>
                            </div>
                        </div>
                    </main>

                    <Footer />
                </div>
            ) : (
                <div className="min-h-screen bg-black text-white flex flex-col">
                    <Header />

                    {/* Centered Main Section */}
                    <main className="flex-grow flex justify-center items-center">
                        {/* Image Container */}
                        <div
                            className="flex flex-col justify-center items-center w-2/3 bg-glass border-2 border-green-400 shadow-glass"
                            style={{ height: '85vh' }} // Adjusted height
                        >
                            {images.length > 0 ? (
                                <img
                                    src={images[currentIndex]}
                                    alt={`Radar ${currentIndex}`}
                                    className="max-h-full max-w-full rounded-lg"
                                />
                            ) : (
                                <p className="text-gray-200">No images available</p>
                            )}
                            <div className="flex justify-center items-center mt-4 space-x-4">
                                <button
                                    className="glass-icon-button"
                                    onClick={handleFirstImage}
                                    title="First Image"
                                >
                                    ⏮️
                                </button>
                                <button
                                    className="glass-icon-button"
                                    onClick={handlePrevImage}
                                    title="Previous Image"
                                >
                                    ◀️
                                </button>
                                <button
                                    className="glass-icon-button"
                                    onClick={togglePlayPause}
                                    title={isPlaying ? 'Pause Slideshow' : 'Play Slideshow'}
                                >
                                    {isPlaying ? '⏸️' : '▶️'}
                                </button>
                                <button
                                    className="glass-icon-button"
                                    onClick={handleNextImage}
                                    title="Next Image"
                                >
                                    ▶️
                                </button>
                                <button
                                    className="glass-icon-button"
                                    onClick={handleLastImage}
                                    title="Last Image"
                                >
                                    ⏭️
                                </button>
                            </div>
                        </div>

                        {/* Metadata Container */}
                        <div
                            className="flex flex-col justify-center items-center w-1/3 bg-glass border-2 border-green-400 shadow-glass p-6"
                            style={{ height: '85vh' }} // Adjusted height
                        >
                            <h2 className="text-xl font-semibold text-green-400 mb-4">
                                Metadata Information
                            </h2>
                            <pre className="text-gray-200">{JSON.stringify(metadata, null, 2)}</pre>
                        </div>
                    </main>

                    <Footer />
                </div>
            )}
        </>
    );
};

export default DataViewer;
