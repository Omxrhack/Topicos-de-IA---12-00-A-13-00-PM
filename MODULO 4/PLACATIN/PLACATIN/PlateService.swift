import Foundation
import UIKit

class PlateService {
    // Cambia la URL por la de tu backend en Render
    private let endpoint = URL(string: "https://plate-backend-mcsd.onrender.com/api/v1/plate/detect")!

    func detectPlate(from image: UIImage, completion: @escaping (Result<PlateDetectionResponse, Error>) -> Void) {
        guard let imageData = image.jpegData(compressionQuality: 0.8) else {
            completion(.failure(NSError(domain: "PlateService", code: -1, userInfo: [NSLocalizedDescriptionKey: "No se pudo convertir la imagen a JPEG"])))
            return
        }

        var request = URLRequest(url: endpoint)
        request.httpMethod = "POST"

        let boundary = "Boundary-\(UUID().uuidString)"
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")

        var body = Data()

        // Campo 'file' como en el backend FastAPI
        let filename = "photo.jpg"
        let mimeType = "image/jpeg"

        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"file\"; filename=\"\(filename)\"\r\n".data(using: .utf8)!)
        body.append("Content-Type: \(mimeType)\r\n\r\n".data(using: .utf8)!)
        body.append(imageData)
        body.append("\r\n".data(using: .utf8)!)
        body.append("--\(boundary)--\r\n".data(using: .utf8)!)

        request.httpBody = body

        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                DispatchQueue.main.async {
                    completion(.failure(error))
                }
                return
            }

            guard let httpResponse = response as? HTTPURLResponse else {
                DispatchQueue.main.async {
                    completion(.failure(NSError(domain: "PlateService", code: -2, userInfo: [NSLocalizedDescriptionKey: "Respuesta inválida del servidor"])))
                }
                return
            }

            guard let data = data else {
                DispatchQueue.main.async {
                    completion(.failure(NSError(domain: "PlateService", code: -3, userInfo: [NSLocalizedDescriptionKey: "Sin datos en la respuesta"])))
                }
                return
            }

            do {
                if (200..<300).contains(httpResponse.statusCode) {
                    let decoded = try JSONDecoder().decode(PlateDetectionResponse.self, from: data)
                    DispatchQueue.main.async {
                        completion(.success(decoded))
                    }
                } else {
                    // Intentar decodificar error del backend
                    let decoded = try? JSONDecoder().decode(PlateDetectionResponse.self, from: data)
                    let message = decoded?.detail ?? "Error del servidor (código \(httpResponse.statusCode))"
                    let err = NSError(domain: "PlateService", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: message])
                    DispatchQueue.main.async {
                        completion(.failure(err))
                    }
                }
            } catch {
                DispatchQueue.main.async {
                    completion(.failure(error))
                }
            }
        }

        task.resume()
    }
}
