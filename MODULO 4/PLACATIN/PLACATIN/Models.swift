import Foundation

struct PlateDetectionResponse: Codable {
    let success: Bool
    let plateText: String?
    let confidence: Double?
    let bbox: BBox?
    let detail: String?  // para errores del backend

    enum CodingKeys: String, CodingKey {
        case success
        case plateText = "plate_text"
        case confidence
        case bbox
        case detail
    }
}

struct BBox: Codable {
    let x: Int
    let y: Int
    let w: Int
    let h: Int
}

struct PlateRecord: Identifiable, Codable {
    let id = UUID()
    let text: String
    let confidence: Double
    let date: Date
}
