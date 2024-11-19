import React, { useState } from "react";
import Footer from "../Components/Footer";
import Header from "../Components/Header";
import RadarAnimation from "../Components/RadarAnimation";

const UploadFile = () => {
	const [file, setFile] = useState(null);
	const [message, setMessage] = useState("");

	const handleFileChange = (e) => {
		setFile(e.target.files[0]);
	};

	const handleUpload = async () => {
		if (!file) {
			setMessage("Please select a file to upload.");
			return;
		}

		const formData = new FormData();
		formData.append("file", file);

		try {
			// write the api calling code here -> eialid
		} catch (error) {
			setMessage("Error uploading file. Please try again.");
		}
	};

	return (
		<div className="min-h-screen flex flex-col bg-black text-white relative overflow-hidden">
			<div className="absolute inset-0 pointer-events-none flex justify-center items-center">
				<RadarAnimation />
			</div>

			<Header />

			<main className="flex-grow flex flex-col justify-center items-center py-8 relative z-10">
				<div
					className="w-[700px] bg-glass border-2 border-green-400 rounded-lg shadow-glass p-6"
					style={{
						backdropFilter: "blur(10px)",
						background: "rgba(255, 255, 255, 0.1)",
					}}
				>
					<h2 className="text-xl font-semibold text-green-400 mb-4">
						Upload File
					</h2>
					<div className="flex flex-col items-center">
						<input
							type="file"
							onChange={handleFileChange}
							className="mb-4 text-gray-200"
						/>
						<button
							className="glass-button"
							onClick={handleUpload}
						>
							Upload
						</button>
					</div>
					{message && (
						<p className="text-green-400 mt-4">{message}</p>
					)}
				</div>
			</main>

			<Footer />
		</div>
	);
};

export default UploadFile;
