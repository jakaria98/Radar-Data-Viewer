import React from "react";
import BackgroundAnimation from "../Components/BackgroundAnimation";
import Footer from "../Components/Footer";
import Header from "../Components/Header";

const DataViewer = () => {
	return (
		<div className="min-h-screen flex flex-col bg-black text-white relative overflow-hidden">
			<div className="absolute inset-0 pointer-events-none flex justify-center items-center">
				<BackgroundAnimation />
			</div>

			{/* Header */}
			<Header />

			{/* Main Content */}
			<main className="flex-grow flex flex-col justify-center items-center py-8 relative z-10">
				<div className="w-[700px] bg-black border-2 border-green-400 rounded-lg shadow-xl p-4">
					<div className="text-right mb-4 flex justify-end gap-2">
						<button className="bg-green-500 text-black px-6 py-2 rounded hover:bg-green-400">
							Load
						</button>

						<button className="bg-green-500 text-black px-6 py-2 rounded hover:bg-green-400">
							Upload
						</button>
					</div>

					{/* Radar Image Viewer */}
					<div className="bg-black border-2 border-green-400 rounded-lg w-full h-[400px] flex justify-center items-center">
						<p className="text-gray-400 text-lg">
							Radar Image Placeholder
						</p>
					</div>

					{/* Image Controls */}
					<div className="flex justify-center items-center mt-4 space-x-4">
						<button className="w-12 h-12 bg-green-500 text-black rounded-full hover:bg-green-400 flex justify-center items-center text-xl">
							◀️◀️
						</button>
						<button className="w-12 h-12 bg-green-500 text-black rounded-full hover:bg-green-400 flex justify-center items-center text-xl">
							◀️
						</button>
						<button className="w-12 h-12 bg-green-500 text-black rounded-full hover:bg-green-400 flex justify-center items-center text-xl">
							| |
						</button>
						<button className="w-12 h-12 bg-green-500 text-black rounded-full hover:bg-green-400 flex justify-center items-center text-xl">
							▶️
						</button>
						<button className="w-12 h-12 bg-green-500 text-black rounded-full hover:bg-green-400 flex justify-center items-center text-xl">
							▶️▶️
						</button>
					</div>
				</div>

				{/* Information of the image*/}
				<div className="w-[700px] bg-black border-2 border-green-400 rounded-lg shadow-xl p-4 mt-8">
					<h2 className="text-xl font-semibold text-green-400 mb-2">
						Information
					</h2>
					<p className="text-gray-300">
						This is a placeholder for the radar image's
						metadata or relevant details. You can include
						information like date, time, radar frequency, or
						any additional properties related to the image
						being displayed.
					</p>
				</div>
			</main>

			{/* Footer */}
			<Footer />
		</div>
	);
};

export default DataViewer;
