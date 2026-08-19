import { useRef, useState } from "react";
import { Camera, Upload, RefreshCw, TriangleAlert, ListChecks } from "lucide-react";
import { useApp } from "../context/AppContext";
import PageContainer from "../components/layout/PageContainer";
import Card from "../components/ui/Card";
import Button from "../components/ui/Button";
import Badge from "../components/ui/Badge";
import { diseaseClasses, supportedCrops } from "../data/mock";

export default function DiseaseDetection() {
  const { t, lang } = useApp();
  const [image, setImage] = useState(null);
  const [status, setStatus] = useState("idle"); // idle | analyzing | done
  const inputRef = useRef(null);
  const result = diseaseClasses[0];

  function onFile(e) {
    const file = e.target.files?.[0];
    if (!file) return;
    setImage(URL.createObjectURL(file));
    setStatus("analyzing");
    // Mocked inference — replace with a real call to the crop-disease model endpoint.
    setTimeout(() => setStatus("done"), 1600);
  }

  function reset() {
    setImage(null);
    setStatus("idle");
    if (inputRef.current) inputRef.current.value = "";
  }

  return (
    <PageContainer>
      <div className="mb-4">
        <h1 className="font-display text-xl font-extrabold text-leaf-900">{t("disease_title")}</h1>
        <p className="text-ink-600 text-sm mt-1">{t("disease_subtitle")}</p>
      </div>

      {status === "idle" && (
        <>
          <Card className="border-2 border-dashed border-leaf-400/60 bg-leaf-100/40 text-center py-10 mb-4">
            <div className="grid place-items-center w-14 h-14 rounded-full bg-leaf-100 text-leaf-800 mx-auto mb-3">
              <Upload size={26} strokeWidth={2} />
            </div>
            <input
              ref={inputRef}
              type="file"
              accept="image/*"
              capture="environment"
              onChange={onFile}
              className="hidden"
              id="leaf-upload"
            />
            <div className="flex flex-col items-center gap-2.5 px-6">
              <Button onClick={() => inputRef.current?.click()} icon={Camera} className="w-full">
                {t("disease_camera")}
              </Button>
              <Button
                onClick={() => inputRef.current?.click()}
                variant="outline"
                icon={Upload}
                className="w-full"
              >
                {t("disease_upload")}
              </Button>
            </div>
          </Card>

          <Card>
            <p className="text-xs font-semibold text-ink-400 uppercase tracking-wide mb-2.5">
              {t("disease_supportedCrops")}
            </p>
            <div className="flex flex-wrap gap-2">
              {supportedCrops.map((c) => (
                <Badge key={c} tone="neutral">{c}</Badge>
              ))}
            </div>
          </Card>
        </>
      )}

      {status !== "idle" && (
        <Card className="mb-4 overflow-hidden" padded={false}>
          <img src={image} alt="Uploaded leaf" className="w-full h-56 object-cover" />
        </Card>
      )}

      {status === "analyzing" && (
        <Card className="text-center py-8">
          <div className="w-8 h-8 mx-auto mb-3 rounded-full border-4 border-leaf-100 border-t-leaf-700 animate-spin" />
          <p className="text-ink-600 text-sm font-medium">{t("disease_analyzing")}</p>
        </Card>
      )}

      {status === "done" && (
        <>
          <Card className="mb-4">
            <div className="flex items-center justify-between mb-2">
              <h3 className="font-display font-bold text-leaf-900 text-base">
                {lang === "hi" ? result.name_hi : result.name_en}
              </h3>
              <Badge tone={result.confidence >= 80 ? "success" : "warning"}>
                {result.confidence}% {t("disease_confidence")}
              </Badge>
            </div>
            <div className="w-full h-2 rounded-full bg-soil-100 overflow-hidden mb-1">
              <div
                className="h-full bg-leaf-600 rounded-full"
                style={{ width: `${result.confidence}%` }}
              />
            </div>
            {result.confidence < 90 && (
              <p className="flex items-start gap-1.5 text-xs text-clay-500 mt-2.5">
                <TriangleAlert size={14} className="shrink-0 mt-0.5" />
                {t("disease_lowConfidence")}
              </p>
            )}
          </Card>

          <Card className="mb-4">
            <p className="flex items-center gap-1.5 font-display font-bold text-leaf-900 text-sm mb-3">
              <ListChecks size={16} /> {t("disease_recommended")}
            </p>
            <ol className="space-y-2.5">
              {(lang === "hi" ? result.actions_hi : result.actions_en).map((a, i) => (
                <li key={i} className="flex gap-2.5 text-sm text-ink-900 leading-snug">
                  <span className="shrink-0 w-5 h-5 grid place-items-center rounded-full bg-leaf-100 text-leaf-800 text-[11px] font-bold">
                    {i + 1}
                  </span>
                  {a}
                </li>
              ))}
            </ol>
          </Card>

          <Button variant="outline" icon={RefreshCw} onClick={reset} className="w-full">
            {t("disease_tryAnother")}
          </Button>
        </>
      )}
    </PageContainer>
  );
}
