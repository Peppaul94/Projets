import fs from "fs";
import http from "http";
import path, { dirname } from "path";
import { fileURLToPath } from "url";

const hostname = "localhost";
const port = process.env.PORT || 4001;

// Emulate __dirname in ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Allow default mode via command-line argument (e.g. `node correction.js mode=2`)
// or environment variable DEFAULT_MODE. Request query `mode` still overrides per-request.
const _cliModeArg = process.argv.slice(2).find(a => a.startsWith("mode="));
const DEFAULT_MODE = (_cliModeArg ? _cliModeArg.split("=")[1] : process.env.DEFAULT_MODE || "2").toLowerCase();

const server = http.createServer((req, res) => {
	const baseURL = "http://" + req.headers.host + "/";
	const reqUrl = new URL(req.url, baseURL);
	const name = reqUrl.searchParams.get("name");
	const mode = (reqUrl.searchParams.get("mode") || DEFAULT_MODE).toLowerCase(); // '1'|'2'|'3' or 'join'|'secure'|'whitelist'
	let content = "";

	// Serve static CSS files requested by path (e.g. /style.css)
	if (reqUrl.pathname && reqUrl.pathname.endsWith('.css')) {
		// Normalize path to prevent leading slash issues
		const rel = reqUrl.pathname.replace(/^\/+/, '');
		const cssJoined = path.join(__dirname, rel);
		const cssResolved = path.resolve(cssJoined);
		const baseDir = path.resolve(__dirname);
		if (!cssResolved.startsWith(baseDir + path.sep) && cssResolved !== baseDir) {
			res.statusCode = 403;
			res.setHeader('Content-Type', 'text/plain');
			res.end('Access denied');
			return;
		}
		try {
			const css = fs.readFileSync(cssResolved, 'utf8');
			res.statusCode = 200;
			res.setHeader('Content-Type', 'text/css');
			res.end(css);
		} catch (e) {
			res.statusCode = 404;
			res.setHeader('Content-Type', 'text/plain');
			res.end('Not Found');
		}
		return;
	}

	if (name) {
		res.setHeader("Content-Type", "text/html");
		// Logging attempt
		console.log(`[INFO] File access attempt: name=${name} mode=${mode} from=${req.socket.remoteAddress}`);

		// Base directory we allow serving files from
		const baseDir = path.resolve(__dirname);

		// Helper to read a file safely and respond
		const sendFile = (filePath) => {
			try {
				content = fs.readFileSync(filePath, "utf8");
				res.statusCode = 200;
				res.end(content);
			} catch (err) {
				res.statusCode = 404;
				res.end("File not found");
			}
		};

		if (mode === "1" || mode === "join") {
			// Solution 1: use path.join(__dirname, name)
			const filePath = path.join(__dirname, name);
			sendFile(filePath);
			return;
		}

		if (mode === "2" || mode === "secure" || mode === "resolve") {
			// Solution 2: path.join + path.resolve and ensure path stays inside baseDir
			const joined = path.join(__dirname, name);
			const resolved = path.resolve(joined);
			const resolvedBase = baseDir.endsWith(path.sep) ? baseDir : baseDir + path.sep;
			if (!resolved.startsWith(resolvedBase) && resolved !== baseDir) {
				res.statusCode = 403;
				res.end("Access denied");
				return;
			}
			sendFile(resolved);
			return;
		}

		if (mode === "3" || mode === "whitelist") {
			// Solution 3: whitelist specific filenames
			const allowedFiles = [
				"web_page.html",
                "web_page2.html",
				"exemple2.txt",
			];
			if (!allowedFiles.includes(name)) {
				res.statusCode = 403;
				res.end("Access denied");
				return;
			}
			const filePath = path.join(__dirname, name);
			sendFile(filePath);
			return;
		}

		// Fallback: behave like secure mode
		const fallbackJoined = path.join(__dirname, name);
		const fallbackResolved = path.resolve(fallbackJoined);
		if (!fallbackResolved.startsWith(baseDir + path.sep) && fallbackResolved !== baseDir) {
			res.statusCode = 403;
			res.end("Access denied");
			return;
		}
		sendFile(fallbackResolved);
	} else {
		res.statusCode = 200;
		res.setHeader("Content-Type", "text/html");
		try {
			content = fs.readFileSync("C:\\Users\\20221292\\Desktop\\Projets-1\\nexa_web_security\\DEFENSE\\pratique\\02-bibliotheque_fs\\web_page.html", "utf8");
		} catch (e) {
			console.log("Error:", e.stack);
		}
		res.end(content);
	}
});

server.listen(port, () => {
	console.log(`Server running at http://${hostname}:${port}/`);
});
