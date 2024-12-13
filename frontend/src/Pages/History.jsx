import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../Components/AuthContext";
import Footer from "../Components/Footer";
import Header from "../Components/Header";
import RadarAnimation from "../Components/RadarAnimation";

export default function History() {
	const navigate = useNavigate();
	const { authState } = useAuth();
	useEffect(() => {
		console.log(authState.isAdmin);
		if (!authState.isLoggedIn) {
			console.log("Not Logged In");
			navigate("/login");
			return;
		}
	}, [authState.isLoggedIn, navigate]);

	const [historyFiles, setHistoryFiles] = useState([]);
	const [error, setError] = useState("");

	useEffect(() => {
		const fetchHistory = async () => {
			try {
				const response = await fetch(
					"http://127.0.0.1:8000/api/files/",
					{
						method: "GET",
						headers: {
							Authorization: `Token ${localStorage.getItem(
								"authToken"
							)}`,
						},
					}
				);

				const data = await response.json();
				if (response.ok) {
					console.log(data);
					setHistoryFiles(data?.files);
				} else {
					setError(data.message || "Failed to fetch.");
				}
			} catch (err) {
				setError("An error occured");
			}
		};

		fetchHistory();
	}, []);

	const handleSingleFile = async (fID) => {
		try {
			const res = await fetch(
				`http://127.0.0.1:8000/api/files/${fID}/`,
				{
					method: "GET",
					headers: {
						Authorization: `Token ${localStorage.getItem(
							"authToken"
						)}`,
					},
				}
			);

			const data = await res.json();

			if (res.ok) {
				navigate("/home", { state: { data } });
			} else {
				console.error("Failed to fetch: ", data.message);
			}
		} catch (err) {
			console.error("Error fetching: ", err);
		}
	};

	return (
		<div className="min-h-screen flex flex-col bg-black text-white relative overflow-hidden">
			<div className="absolute inset-0 pointer-events-none flex justify-center items-center">
				<RadarAnimation />
			</div>

			<Header />

			<main className="flex-grow flex flex-col items-center justify-center py-8 relative z-10">
				{historyFiles.length === 0 && (
					<div className="text-red-500 bg-black border border-red-500 rounded-lg p-4 mb-4">
						You don't have any previously uploaded files.
					</div>
				)}

				{historyFiles.length > 0 && (
					<>
						<h1 className="text-4xl font-bold text-green-400 mb-8 text-center">
							Previously Uploaded Files
						</h1>
						<div
							className="w-[90%] max-w-4xl bg-glass border-2 border-green-400 rounded-lg shadow-glass p-6"
							style={{
								backdropFilter: "blur(10px)",
								background: "rgba(255, 255, 255, 0.1)",
							}}
						>
							<table className="w-full text-left border-separate border-spacing-y-4">
								<thead
									className="bg-glass text-white font-medium shadow-glass"
									style={{
										backdropFilter: "blur(10px)",
										background:
											"rgba(255, 255, 255, 0)",
									}}
								>
									<tr>
										<th className="px-6 py-4 text-center">
											File Name
										</th>
										<th className="px-6 py-4 text-center">
											Uploaded At
										</th>
									</tr>
								</thead>
								<tbody>
									{historyFiles.length > 0 ? (
										historyFiles.map(
											(hfile, index) => (
												<tr
													key={index}
													className="bg-glass text-green-400 shadow-glass hover:text-white"
													style={{
														backdropFilter:
															"blur(10px)",
														background:
															"rgba(255, 255, 255, 0)",
													}}
												>
													<td
														className="px-6 py-4 text-center underline cursor-pointer"
														onClick={() =>
															handleSingleFile(
																hfile.id
															)
														}
													>
														{
															hfile.filename
														}
													</td>
													<td className="px-6 py-4 text-center">
														{
															hfile.uploaded_at
														}
													</td>
												</tr>
											)
										)
									) : (
										<tr>
											<td
												colSpan="4"
												className="px-6 py-4 text-center text-gray-400"
											>
												No history available
											</td>
										</tr>
									)}
								</tbody>
							</table>
						</div>
					</>
				)}
			</main>

			<Footer />
		</div>
	);
}
