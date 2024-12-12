import React, { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../Components/AuthContext";
import Footer from "../Components/Footer";
import Header from "../Components/Header";
import RadarAnimation from "../Components/RadarAnimation";

const DataViewer = () => {
	const navigate = useNavigate();
	const location = useLocation();
	const [images, setImages] = useState([]);
	const [metadata, setMetadata] = useState({});
	const [currentIndex, setCurrentIndex] = useState(0);
	const [isPlaying, setIsPlaying] = useState(true); // State to control play/pause
	const radarData = location.state && location.state.data;
	console.log(radarData);
	const { authState } = useAuth();
	useEffect(() => {
		if (!authState.isLoggedIn) {
			navigate("/login");
		}
	}, [authState.isLoggedIn, navigate]);

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
				setCurrentIndex(
					(prevIndex) => (prevIndex + 1) % images.length
				);
			}, 3000); // Change image every 3 seconds
		}
		return () => clearInterval(interval);
	}, [images, isPlaying]);

	// Navigate to previous and next images
	const handlePrevImage = () => {
		setCurrentIndex(
			(prevIndex) => (prevIndex - 1 + images.length) % images.length
		);
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

	// formating the metadata
	const formatMetadata = (metadata) => {
		const metadataMap = {
			num_samples: "Number of Samples",
			frequency: "Frequency",
			year: "Year",
			range_resolution: "Range Resolution",
			true_north: "True North",
			rate: "Rate",
			num_ranges: "Number of Ranges",
			num_antennas: "Number of Antennas",
			latitude: "Latitude",
			longitude: "Longitude",
			mt: "Maximum Transmission (MT)",
			pwr: "Power (PWR)",
			md: "Mode (MD)",
			offset: "Offset",
			rx_offset: "Receiver Offset (RXOFFSET)",
			heading: "Heading (HD)",
			timestamp: "Timestamp",
		};

		const units = {
			num_samples: "samples",
			frequency: "MHz",
			year: "year",
			range_resolution: "km",
			true_north: "degrees",
			rate: "seconds",
			num_ranges: "ranges",
			num_antennas: "antennas",
			latitude: "degrees",
			longitude: "degrees",
			mt: "unknown",
			pwr: "power units",
			md: "unknown",
			offset: "units",
			rx_offset: "units",
			heading: "degrees",
			timestamp: "",
		};

		return Object.entries(metadata).map(([key, value]) => {
			const label = metadataMap[key] || key;
			const unit = units[key] || "";
			return `${label}: ${value} ${unit}`.trim();
		});
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
						<div
							className="w-[750px] max-w-full bg-glass border-[3px] border-green-400 rounded-xl shadow-glass p-8 text-center transform transition duration-300 hover:scale-105"
							style={{
								backdropFilter: "blur(15px)",
								background: "rgba(255, 255, 255, 0.1)", // Keeps the glass effect
							}}
						>
							<h1 className="text-3xl font-bold text-green-400 mb-6">
								No Data Available
							</h1>
							<p className="text-gray-300 text-lg mb-8 leading-relaxed">
								You currently don’t have any radar data
								loaded. Start by uploading your radar
								file to explore the data seamlessly in
								our viewer.
							</p>

							<div className="w-16 h-[2px] bg-green-400 mx-auto mb-6"></div>

							<div className="flex justify-center">
								<button
									className="glass-button px-8 py-3 text-lg font-medium rounded-full border-[2px] border-green-400 shadow-md shadow-green-400/50 hover:shadow-lg hover:shadow-green-500/70 transition-all duration-300"
									onClick={() => navigate("/upload")}
								>
									Upload File
								</button>
							</div>
						</div>
					</main>

					<Footer />
				</div>
			) : (
				<div className="min-h-screen bg-black text-white flex flex-col relative overflow-hidden">
					<div className="absolute inset-0 pointer-events-none flex justify-center items-center">
						<RadarAnimation />
					</div>

					<Header />

					<main className="flex-grow flex flex-col justify-center items-center py-8 relative z-10">
						<div className="flex justify-center items-start w-[80%] space-x-8">
							<div
								className="w-1/2 bg-glass border-2 border-green-400 rounded-lg shadow-glass p-4"
								style={{
									backdropFilter: "blur(10px)",
									background:
										"rgba(255, 255, 255, 0.1)",
								}}
							>
								{images.length > 0 ? (
									<img
										src={images[currentIndex]}
										alt={`Radar ${currentIndex}`}
										className="w-full rounded-lg border border-green-400 shadow-md"
									/>
								) : (
									<p className="text-gray-200 text-lg text-center">
										No images available
									</p>
								)}

								<div className="flex justify-center items-center mt-4 space-x-4">
									<button
										className="glass-icon-button"
										onClick={handleFirstImage}
										title="First Image"
									>
										◀️◀️
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
										title={
											isPlaying
												? "Pause Slideshow"
												: "Play Slideshow"
										}
									>
										{isPlaying ? "| |" : "▶️"}
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
										▶️▶️
									</button>
								</div>
							</div>

							<div
								className="w-1/2 bg-glass border-2 border-green-400 rounded-lg shadow-glass p-6"
								style={{
									backdropFilter: "blur(10px)",
									background:
										"rgba(255, 255, 255, 0.1)",
								}}
							>
								<h2 className="text-xl font-semibold text-green-400 mb-4">
									Image Metadata
								</h2>
								<table className="w-full text-left text-gray-200">
									<tbody>
										{metadata
											? Object.entries(
													metadata
											  ).map(
													([
														key,
														value,
													]) => (
														<tr
															key={
																key
															}
														>
															<td className="py-2 pr-4 font-semibold text-green-400">
																{
																	key
																}

																:
															</td>
															<td className="py-2">
																{typeof value ===
																"object"
																	? JSON.stringify(
																			value,
																			null,
																			2
																	  )
																	: value}
															</td>
														</tr>
													)
											  )
											: "No metadata available"}
									</tbody>
								</table>
							</div>
						</div>
					</main>

					<Footer />
				</div>
			)}
		</>
	);
};

export default DataViewer;
