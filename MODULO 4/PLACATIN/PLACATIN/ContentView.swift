import SwiftUI


struct ContentView: View {
    @State private var selectedImage: UIImage?
    @State private var showCamera = false
    @State private var showGallery = false
    @State private var isDetecting = false
    @State private var detectionResult: PlateDetectionResponse?
    @State private var errorMessage: String?
    @State private var records: [PlateRecord] = []

    private let service = PlateService()

    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 16) {
                    // Imagen seleccionada
                    if let selectedImage = selectedImage {
                        Image(uiImage: selectedImage)
                            .resizable()
                            .scaledToFit()
                            .frame(maxHeight: 250)
                            .cornerRadius(12)
                            .shadow(radius: 5)
                    } else {
                        ZStack {
                            RoundedRectangle(cornerRadius: 12)
                                .strokeBorder(style: StrokeStyle(lineWidth: 1, dash: [5]))
                                .foregroundColor(.gray)
                                .frame(height: 200)

                            Text("Selecciona o toma una foto de la placa")
                                .foregroundColor(.gray)
                                .multilineTextAlignment(.center)
                                .padding()
                        }
                    }

                    HStack(spacing: 16) {
                        Button(action: {
                            showCamera = true
                        }) {
                            HStack {
                                Image(systemName: "camera")
                                Text("Cámara")
                            }
                            .frame(maxWidth: .infinity)
                        }
                        .buttonStyle(.borderedProminent)

                        Button(action: {
                            showGallery = true
                        }) {
                            HStack {
                                Image(systemName: "photo")
                                Text("Galería")
                            }
                            .frame(maxWidth: .infinity)
                        }
                        .buttonStyle(.bordered)
                    }

                    Button(action: detectPlate) {
                        if isDetecting {
                            ProgressView()
                                .progressViewStyle(CircularProgressViewStyle())
                                .frame(maxWidth: .infinity)
                        } else {
                            HStack {
                                Image(systemName: "viewfinder")
                                Text("Detectar placa")
                            }
                            .frame(maxWidth: .infinity)
                        }
                    }
                    .buttonStyle(.borderedProminent)
                    .disabled(selectedImage == nil || isDetecting)

                    if let result = detectionResult, result.success, let text = result.plateText {
                        VStack(alignment: .leading, spacing: 8) {
                            Text("Resultado de la detección")
                                .font(.headline)

                            Text("Placa: \(text)")
                                .font(.title3)
                                .fontWeight(.bold)

                            if let confidence = result.confidence {
                                Text(String(format: "Confianza: %.2f", confidence))
                                    .font(.subheadline)
                                    .foregroundColor(.secondary)
                            }

                            Button(action: { saveRecord(from: result) }) {
                                HStack {
                                    Image(systemName: "tray.and.arrow.down")
                                    Text("Guardar placa")
                                }
                                .frame(maxWidth: .infinity)
                            }
                            .buttonStyle(.bordered)
                        }
                        .padding()
                        .background(Color(.systemGray6))
                        .cornerRadius(12)
                    }

                    if let errorMessage = errorMessage {
                        Text(errorMessage)
                            .foregroundColor(.red)
                            .multilineTextAlignment(.center)
                    }

                    if !records.isEmpty {
                        VStack(alignment: .leading, spacing: 8) {
                            Text("Historial de placas")
                                .font(.headline)

                            ForEach(records) { record in
                                VStack(alignment: .leading) {
                                    Text(record.text)
                                        .font(.body)
                                        .fontWeight(.semibold)
                                    Text(String(format: "Confianza: %.2f", record.confidence))
                                        .font(.caption)
                                        .foregroundColor(.secondary)
                                    Text(record.date, style: .date)
                                        .font(.caption2)
                                        .foregroundColor(.secondary)
                                }
                                .padding(8)
                                .background(Color(.systemGray6))
                                .cornerRadius(8)
                            }
                        }
                        .padding(.top)
                    }
                }
                .padding()
            }
            .navigationTitle("Detector de Placas")
        }
        .sheet(isPresented: $showCamera) {
            ImagePicker(image: $selectedImage, sourceType: .camera)
        }
        .sheet(isPresented: $showGallery) {
            ImagePicker(image: $selectedImage, sourceType: .photoLibrary)
        }
    }

    private func detectPlate() {
        guard let image = selectedImage else { return }
        isDetecting = true
        errorMessage = nil
        detectionResult = nil

        service.detectPlate(from: image) { result in
            isDetecting = false
            switch result {
            case .success(let response):
                detectionResult = response
                if response.success == false {
                    errorMessage = response.detail ?? "No se pudo detectar la placa."
                }
            case .failure(let error):
                errorMessage = error.localizedDescription
            }
        }
    }

    private func saveRecord(from response: PlateDetectionResponse) {
        guard let text = response.plateText else { return }
        let confidence = response.confidence ?? 0.0
        let record = PlateRecord(text: text, confidence: confidence, date: Date())
        records.insert(record, at: 0)
    }
}

#Preview {
    ContentView()
}
