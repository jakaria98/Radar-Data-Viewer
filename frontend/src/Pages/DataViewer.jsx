import React from "react";
import Footer from "../Components/Footer";
import Header from "../Components/Header";
import RadarAnimation from "../Components/RadarAnimation";

const DataViewer = () => {
	return (
		<div className="min-h-screen flex flex-col bg-black text-white relative overflow-hidden">
			<div className="absolute inset-0 pointer-events-none flex justify-center items-center">
				<RadarAnimation />
			</div>

			<Header />

			<main className="flex-grow flex flex-col justify-center items-center py-8 relative z-10">
				<div
					className="w-[700px] bg-glass border-2 border-green-400 rounded-lg shadow-glass p-4"
					style={{
						backdropFilter: "blur(10px)",
						background: "rgba(255, 255, 255, 0.1)",
					}}
				>
					<div className="text-right mb-4 flex justify-end gap-2">
						<button className="glass-button">Load</button>
						<button className="glass-button">Upload</button>
					</div>

					<div
						className="bg-glass border-2 border-green-400 rounded-lg w-full h-[400px] flex justify-center items-center"
						style={{
							backdropFilter: "blur(10px)",
							background: "rgba(255, 255, 255, 0.1)",
						}}
					>
						<p className="text-gray-200 text-lg">
							Radar Image Placeholder
						</p>
					</div>

					<div className="flex justify-center items-center mt-4 space-x-4">
						<button className="glass-icon-button">
							◀️◀️
						</button>
						<button className="glass-icon-button">◀️</button>
						<button className="glass-icon-button">| |</button>
						<button className="glass-icon-button">▶️</button>
						<button className="glass-icon-button">
							▶️▶️
						</button>
					</div>
				</div>

				<div
					className="w-[700px] bg-glass border-2 border-green-400 rounded-lg shadow-glass p-4 mt-8"
					style={{
						backdropFilter: "blur(10px)",
						background: "rgba(255, 255, 255, 0.1)",
					}}
				>
					<h2 className="text-xl font-semibold text-green-400 mb-2">
						Information
					</h2>
					<p className="text-gray-200">
						This is a placeholder for the radar image's
						metadata or relevant details. You can include
						information like date, time, radar frequency, or
						any additional properties related to the image
						being displayed.
					</p>
				</div>
			</main>

			<Footer />
		</div>
	);
};

export default DataViewer;
