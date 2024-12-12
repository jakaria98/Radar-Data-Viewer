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

	const [historyFiles, setHistoryFiles] = useState(["dsdsds"]);

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
								<tbody>
									<tr
										className="bg-glass text-green-400 shadow-glass hover:text-white"
										style={{
											backdropFilter:
												"blur(10px)",
											background:
												"rgba(255, 255, 255, 0)",
										}}
									>
										<td className="px-6 py-4">
											Lorem ipsum dolor sit
											amet consectetur
											adipisicing elit. Iusto
											impedit assumenda
											provident, laborum
											ratione tempore?
										</td>
									</tr>
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
