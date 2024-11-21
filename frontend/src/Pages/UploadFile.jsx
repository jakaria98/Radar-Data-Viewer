import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Footer from "../Components/Footer";
import Header from "../Components/Header";
import RadarAnimation from "../Components/RadarAnimation";

const UploadFile = () => {
	const [file, setFile] = useState(null);
	const [message, setMessage] = useState("");
	const navigate = useNavigate();

	const handleFileChange = (e) => {
		setFile(e.target.files[0]);
	};

	const handleUpload = async () => {
		if (!file) {
			setMessage("Please select a file to upload.");
			return;
		}
	
		const formData = new FormData();
		formData.append("file", file); // Ensure the key matches "file" in your Django view
	
		try {
			console.log("Sending.......... ........ ........")
			const response = await fetch("http://127.0.0.1:9000/api/upload/", {
				method: "POST",
				body: formData,
				headers: {
				},
			});
	
			if (response.ok) {
				console.log("Got Response!!")
				const data = await response.json();
				setMessage("File uploaded successfully!");
				navigate("/", { state: { data } }); // Pass response data
				console.log("Response:", data); // Log backend response for debugging
			} else {
				console.log("Errrrrorrrrrrr.....")
				const errorData = await response.json();
				setMessage(`Failed to upload file: ${errorData.message || "Unknown error"}`);
			}
		} catch (error) {
			console.error("Error uploading file:", error);
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
						<div className="relative mb-4">
							<input
								type="file"
								onChange={handleFileChange}
								className="hidden"
								id="fileInput"
							/>
							<label
								htmlFor="fileInput"
								className="glass-button cursor-pointer"
							>
								{file ? file.name : "Choose File"}
							</label>
						</div>
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
