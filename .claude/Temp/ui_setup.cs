using UnityEngine;
using UnityEditor;
using UnityEngine.UI;
using TMPro;
using System.IO;

public class Script
{
    public static object Main()
    {
        try
        {
            string repoRoot = Directory.GetCurrentDirectory();
            string assetsPath = Path.Combine(repoRoot, "Assets/_RhythmRatio");
            string uiPrefabPath = Path.Combine(assetsPath, "UI/Prefabs/MainUI.prefab");

            // 1. Ensure directories exist
            if (!Directory.Exists(Path.Combine(assetsPath, "UI/Scripts")))
                Directory.CreateDirectory(Path.Combine(assetsPath, "UI/Scripts"));
            if (!Directory.Exists(Path.Combine(assetsPath, "UI/Prefabs")))
                Directory.CreateDirectory(Path.Combine(assetsPath, "UI/Prefabs"));

            // 2. Create a temporary scene for setup if needed, or use active scene
            GameObject canvasGo = new GameObject("MainUI_Canvas");
            canvasGo.AddComponent<Canvas>();
            canvasGo.AddComponent<CanvasScaler>();
            canvasGo.AddComponent<GraphicRaycaster>();

            Canvas canvas = canvasGo.GetComponent<Canvas>();
            canvas.renderMode = RenderMode.ScreenSpaceOverlay;

            // 3. Create StartScreen Panel
            GameObject startPanel = new GameObject("StartScreen");
            start.transform.SetParent(canvasGo.transform, false);
            Image startImg = startPanel.AddComponent<Image>();
            startImg.color = new Color(0, 0, 0, 0.5f); // Semi-transparent black

            GameObject startTextGo = new GameObject("StartText");
            startTextGo.transform.SetParent(startPanel.transform, false);
            TextMeshProUGUI startText = startTextGo.AddComponent<TextMeshProUGUI>();
            startText.text = "Tap to Start";
            startText.alignment = TextAlignmentOptions.Center;
            startText.fontSize = 72;

            GameObject highScoreTextGo = new GameObject("HighScoreText");
            highScoreTextGo.transform.SetParent(startPanel.transform, false);
            TextMeshProUGUI highScoreText = highScoreTextGo.AddComponent<TextMeshProUGUI>();
            highScoreText.alignment = TextAlignmentOptions.Center;
            highScoreText.fontSize = 40;

            // 4. Create GameOverScreen Panel
            GameObject gameOverPanel = new GameObject("GameOverScreen");
            gameOverPanel.transform.SetParent(canvasGo.transform, false);
            Image gameOverImg = gameOverPanel.AddComponent<Image>();
            gameOverImg.color = new Color(1, 0, 0, 0.5f); // Semi-transparent red

            GameObject gameOverTextGo = new GameObject("GameOverText");
            gameOverTextGo.transform.SetParent(gameOverPanel.transform, false);
            TextMeshProUGUI gameOverText = gameOverTextGo.AddComponent<TextMeshProUGUI>();
            gameOverText.text = "Game Over";
            gameOverText.alignment = TextAlignmentOptions.Center;
            gameOverText.fontSize = 72;

            GameObject finalScoreTextGo = new GameObject("FinalScoreText");
            finalScoreTextGo.transform.SetParent(gameOverPanel.transform, false);
            TextMeshProUGUI finalScoreText = finalScoreTextGo.AddComponent<TextMeshProUGUI>();
            finalScoreText.alignment = TextAlignmentOptions.Center;
            finalScoreText.fontSize = 40;

            // 5. Create GameplayHUD Panel
            GameObject hudPanel = new GameObject("GameplayHUD");
            hudPanel.transform.SetParent(canvasGo.transform, false);
            GameObject scoreTextGo = new GameObject("ScoreText");
            scoreTextGo.transform.SetParent(hudPanel.transform, false);
            TextMeshProUGUI scoreText = scoreTextGo.AddComponent<TextMeshProUGUI>();
            scoreText.alignment = TextAlignmentOptions.Center;
            scoreText.fontSize = 40;

            // 6. Save as Prefab
            PrefabUtility.SaveAsPrefabAsset(canvasGo, uiPrefabPath);

            // Cleanup
            Object.DestroyImmediate(canvasGo);
            AssetDatabase.Refresh();

            return "Successfully created UI Canvas Prefint at: " + uiPrefabPath;
        }
        catch (System.Exception e)
        {
            return "Error: " + e.Message;
        }
    }
}
