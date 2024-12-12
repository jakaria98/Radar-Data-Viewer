import { useNavigate } from "react-router-dom";
import { useAuth } from "../Components/AuthContext";

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
	return <></>;
}
